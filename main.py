import sys
import requests



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




def get_html(url):
    














if __name__ == "__main__":
    main()
