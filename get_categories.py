from bs4 import BeautifulSoup
import json
from pprint import pprint
from datetime import datetime
import csv
import time
import requests

def getSoup(link):
    req = requests.get(link)
    html = req.content
    soup = BeautifulSoup(html, "html.parser")
    return soup

def get_category(categories, link):
    soup = getSoup(link)
    cat = soup.find("ul", {"id": "plp-list-description"})
    if cat == None:
        cat = soup.find("div", {"id": "plp-thumbs"})

    if cat == None:
        print(link)
        categories.append(link)
        return categories

    items = soup.findAll("div", {"class": "plp-list-thumb"})
    if not items:
        items = soup.findAll("div", {"class": "ui-widget-content ui-corner-all plp-thumb"})
    for item in items:
        item = "https://cad.timken.com"+item.find("a")['href']
        get_category(categories, item)


def get_category_driver():
    link = "https://cad.timken.com/category/"
    categories = []
    categories_json = {}
    get_category(categories, link)
    categories_json["details"] = categories
    with open("categories.json", "w") as f:
        json.dump(categories_json, f)

if __name__ == "__main__":
    # link = "https://cad.timken.com/category/corrosion-resistant-ball-bearing-housed-unit"
    # soup = getSoup(link)
    # print(soup.findAll("div", {"class": "plp-list-thumb"}))

    get_category_driver()