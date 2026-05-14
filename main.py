import sys
from crawl import *
import asyncio
import async_crawler as ac
from json_report import write_json_report



async def main():
    print("Hello from webcrawler!")
    args = sys.argv 
    if len(args) < 2:
        print("no website provided")
        exit(1)
    if len(args) > 4: 
        print("too many arguments provided")
        exit(1)
    base_url = args[1]
    max_concurrency = int(args[2]) or 3
    max_pages = int(args[3]) or 25
    print(f"starting crawl of: {base_url}")
    
    results:dict = await ac.crawl_site_async(base_url,max_concurrency,max_pages)
    write_json_report(results)
    
    print(results)
    print(f"Number of pages crawled: {len(results)}")
    for key in results.keys():
        print(f"- {results[key].get("url","ö-ö")}")
        

















if __name__ == "__main__":
    asyncio.run(main())
