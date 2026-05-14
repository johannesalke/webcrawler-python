
import urllib.parse as parse
import os.path 
from bs4 import BeautifulSoup



def normalize_url(url):
    parsed_url= parse.urlparse(url)
    pth = parsed_url.path.strip("/")
    return os.path.join( parsed_url.netloc ,pth)

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
    
    






#Suspicion: Beautiful soups, or at least the find() element extractions, are a more expansive implementation of dictionaries with additional methods to assist in finding and modifying elements and attributes. 






