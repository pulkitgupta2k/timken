from bs4 import BeautifulSoup
import json
from pprint import pprint
from datetime import datetime
import csv
import time
import grequests

def tabulate(csvfile, matrix):
    with open(csvfile, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(matrix)

def getSoup_list(urls):
    MAX_CONNECTIONS = 100
    requests = []
    for x in range(0,len(urls),MAX_CONNECTIONS):
        rs = (grequests.get(u, stream=False) for u in urls[x:x+MAX_CONNECTIONS])
        print(".")
        time.sleep(0.2)
        response = grequests.map(rs)
        requests.extend(response)
        print(response)
    soups = []
    for request in requests:
        html = request.content
        soup = BeautifulSoup(html, "html.parser")
        soups.append(soup)
    return soups

def get_prod_inf(soup):
    return_list = []
    web_link = soup.find("link")['href']
    item_no = web_link.split('/')[-1].upper()
    categories = []
    for category in soup.find("nav", {"id": "plp-bread-crumb"}).findAll("a")[5:-1]:
        categories.append(category.text)

    for table in soup.findAll("div", {"class": "plp-item-specs"})[1].findAll('div', {'class': 'group'}):
        table_header = table.find("a")['name']
        for tr in table.findAll("tr"):
            criteria = tr.findAll('td')[0].text.strip()
            mul_values = tr.findAll('td')[-1].findAll('span', {'itemprop': "value"})
            for values in mul_values:
                values = values.text.strip()
                value = values
                units = ""
                data = []
                if len(value.split()) == 2:
                    if not values.split()[0].isalnum():
                        value = values.split()[0]
                        units = values.split()[1]
                    else:
                        try:
                            value = float(values.split()[0])
                            units = values.split()[1]
                        except:
                            pass
                data.append(item_no)
                data.append(criteria)
                data.append(value)
                data.append(units)
                data.append(table_header)
                data.append("")
                data.append(item_no+"-Timken-1.jpg")
                data.append(item_no+"-Timken-2.jpg")
                data.append(item_no+"-Timken-3.jpg")
                data.append(item_no+"-Timken.pdf")
                data.append(item_no+"-Timken.dxf")
                data.append(web_link)
                data.extend(categories)

                return_list.append(data)
    return return_list

def get_all_information():
    with open('products.json') as f:
        product_links = json.load(f)
    
    ctr = 0
    links = []
    for product_link in product_links:
        ctr = ctr+1
        links.append(product_link)
        if not ctr % 400:
            soups = getSoup_list(links)
            for soup in soups:
                tabulate('details.csv',get_prod_inf(soup))
            links = []
    print(product_links)

if __name__ == "__main__":
    # soup = getSoup_list(["https://cad.timken.com/item/quiklean--corrosion-resistant-housed-units1/ic-two-bolt-flanged-housed-units-set-screw-locking/sucbflqk204-12"])[0]
    # get_prod_inf(soup)
    get_all_information()