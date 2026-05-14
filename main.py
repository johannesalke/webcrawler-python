import sys

from crawl import *




def main():
    print("Hello from webcrawler!")
    args = sys.argv 
    if len(args) < 2:
        print("no website provided")
        exit(1)
    if len(args) > 2: 
        print("too many arguments provided")
        exit(1)
    base_url = args[1]
    print(f"starting crawl of: {base_url}")
    #html= get_html(base_url)
    #print(html)
    results:dict = crawl_page(base_url)
    print(f"Number of pages crawled: {len(results)}")
    for key in results.keys():
        print(f"- {results[key]["url"]}")
        

















if __name__ == "__main__":
    main()
