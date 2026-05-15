
import urllib.parse as parse
import os.path 
from bs4 import BeautifulSoup
import requests

def normalize_url(url):
    parsed_url= parse.urlparse(url)
    pth = parsed_url.path.strip("/")
    return str(os.path.join( parsed_url.netloc ,pth))

def get_heading_from_html(html):
    soup = BeautifulSoup(html,"html.parser")
    heading_html = soup.find("h1")

    if heading_html is None:
        heading_html = soup.find("h2")
    if heading_html is None:
        return ""
    html = heading_html.get_text()
    return html

def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html,"html.parser")
    main = soup.find("main")
    
    if main:
        
        paragraph = main.find("p")
        
    else:
        paragraph = soup.find("p")

    if paragraph:
        text = paragraph.get_text()
    else: 
        text = ""
    
    return text


def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html,"html.parser")
    
    a_links = soup.find_all("a")
    hrefs = []
    if a_links:
        hrefs = [link.get("href") for link in a_links]
    
    results = [parse.urljoin(base_url,url)for url in hrefs]
    #print(results)
    return results


def get_images_from_html(html,base_url):
    soup = BeautifulSoup(html,"html.parser")
    images = soup.find_all("img")
    img_srcs = []
    if images:
        img_srcs = [image.get("src") for image in images]
    results = [parse.urljoin(base_url,url)for url in img_srcs]
    return results

def get_all_links_from_html(html,base_url):
    soup = BeautifulSoup(html,"html.parser")
    images = soup.find_all("img")
    img_srcs = []
    if images:
        img_srcs = [image.get("src") for image in images]
    a_links = soup.find_all("a")
    hrefs = []
    if a_links:
        hrefs = [link.get("href") for link in a_links]

    results = [parse.urljoin(base_url,url)for url in hrefs+img_srcs]
    return results

def extract_page_data(html,page_url):
    heading = get_heading_from_html(html)
    first_paragraph = get_first_paragraph_from_html(html)
    links = get_urls_from_html(html,page_url)
    image_urls = get_images_from_html(html,page_url)
    page = {}
    page["url"] = page_url
    page["heading"] = heading 
    page["first_paragraph"] = first_paragraph
    page["outgoing_links"] = links 
    page["image_urls"] = image_urls 
    return page

    
def get_html(url):
    res = requests.get(url,headers={"User-Agent":"BootCrawler/1.0"})
    if res.status_code >= 400:
        raise Exception(f"Error on making request: {res.status_code}")
    if "text/html" not  in res.headers.get("content-type",""):
        raise Exception(f"Content type isn't text/html. Instead it is: {res.headers.get("content-type")}")
    html = res.text
    return html



def crawl_page(base_url,current_url=None,page_data=None):
    if page_data is None:
        page_data = {}
    if current_url is None:
        current_url = base_url
    if base_url not in current_url:
        return page_data
    norm = normalize_url(current_url)
    if norm in page_data.keys():
        return page_data
    html = get_html("https://"+norm) 
    print(f"Got html for {norm}")
    data = extract_page_data(html,current_url)   
    page_data[norm] = data
    links = data.get("outgoing_links",[])
    for link in links:
        page_data = crawl_page(base_url,link,page_data)
    return page_data    






















