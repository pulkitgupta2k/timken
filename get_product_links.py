from bs4 import BeautifulSoup
import json
import requests
from pprint import pprint

def getSoup(link):
    req = requests.get(link)
    html = req.content
    soup = BeautifulSoup(html, "html.parser")
    return soup

def get_products(cat_link):
    product_links = []
    i = 0
    while True:
        i = i+1
        flag = 0
        link = cat_link + "?pagesize=200&pagenum=" + str(i)
        soup = getSoup(link)
        page_links = soup.findAll("a", {"class": "plp-itemlink"})
        # print(page_links)
        for page_link in page_links:
            page_link = "https://cad.timken.com" + page_link['href']
            if page_link in product_links:
                flag = 1
                break
            else:
                product_links.append(page_link)
        if flag == 1:
            break
    return product_links

def driver_product_links():
    with open("categories.json") as f:
        categories = json.load(f)['details']
    product_links = []
    for category in categories:
        try:
            print(category)
            product_links.extend(get_products(category))
        except Exception as e:
            print(e)
    with open("products.json") as f:
        json.dump(product_links, f)

if __name__ == "__main__":
    # get_products("https://cad.timken.com/viewitems/corrosion-resistant-poly-round--plain-bearing-hous/corrosion-resistant-round-flanged-housed-unit-poly")
    driver_product_links