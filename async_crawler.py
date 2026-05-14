import asyncio 
import aiohttp
from crawl import *
import urllib.parse as parse




class AsyncCrawler():
    
    def __init__(self, base_url, page_data = {}, max_concurrency = 5,max_pages = 100):
        self.base_url = base_url
        self.base_domain = parse.urlparse(base_url).netloc
        self.page_data = page_data
        self.lock = asyncio.Lock()
        self.semaphore = asyncio.Semaphore(max_concurrency)
        #self.max_concurrency = max_concurrency
        self.session = None
        self.max_pages:int = max_pages
        self.should_stop = False 
        self.all_tasks:set[asyncio.Task[None]] = set()
        

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self 
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        if  self.should_stop == True:
            return False
        async with self.lock:
            if normalized_url in self.page_data.keys():
                return False 
            elif parse.urlparse("https://"+normalized_url).netloc != self.base_domain:
                return False
            elif len(self.page_data) >= self.max_pages:
                self.should_stop = True 
                print("Reached maximum number of pages to crawl")
                #for task in self.all_tasks:
                #    task.cancel()
                return False
            else:
                self.page_data[normalized_url] = {}
                return True
            
    async def get_html(self,url):
        async with self.session.get(url,headers={"User-Agent":"BootCrawler/1.0"}) as res:
        
            if res.status >= 400:
                raise Exception(f"Error on making request: {res.status}")
            if "text/html" not  in res.headers.get("content-type",""):
                raise Exception(f"Content type isn't text/html. Instead it is: {res.headers.get("content-type")}")
            html = await res.text()
        return html
    
    async def crawl_page(self,current_url=None):
        if self.should_stop == True:
            return
        try:
            norm = normalize_url(current_url)
            if not await self.add_page_visit(norm):
                return 
            base_url = self.base_url
            if current_url is None:
                current_url = base_url
            if base_url not in current_url:
                return 
            async with self.semaphore:

                html = await self.get_html("https://"+norm) 
                print(f"Got html for {norm}")
                data = extract_page_data(html,current_url)   
                async with self.lock:
                    self.page_data[norm] = data
                links = data.get("outgoing_links",[])
                tasks = []
                for link in links:
                    task = asyncio.create_task(self.crawl_page(link))
                    tasks.append(task)
                    
                    self.all_tasks.add(task)
            await asyncio.gather(*tasks, return_exceptions=True)
        finally:
            self.all_tasks.discard(asyncio.current_task())
        return    
    
    async def crawl(self,base_url):
        self.base_url = base_url
        await self.crawl_page(self.base_url)
        return self.page_data



async def crawl_site_async(url,max_concurrency = 5,max_pages=25):
    #crawler = AsyncCrawler(url,{},concurrency)
    async with AsyncCrawler(url,{},max_concurrency,max_pages) as crawler:
        results = await crawler.crawl(url)
        return results
