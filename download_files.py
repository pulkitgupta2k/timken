from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import json
import os, os.path
import time

def download_pdf():
    temp_loc = 'temp/'
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    prefs = {"profile.default_content_settings.popups": 0,
                "download.default_directory": r"C:\Users\Pulkit\Desktop\Repos\timken\temp\\",
                "directory_upgrade": True}
    options.add_experimental_option("prefs", prefs)
    driver =  webdriver.Chrome('./chromedriver', chrome_options=options)
    with open ("products.json") as f:
        links = json.load(f)
    for link in links:
        name = link.split('/')[-1].upper() + ".pdf"
        driver.get(link)
        driver.find_element_by_xpath("//a[@class=' pdf plp-img-sprite plp-sprite-pdf']").click()

        while(len(os.listdir(temp_loc)) == 0):
            pass

        while(True):
            try:
                if os.listdir(temp_loc)[0].split('.')[-1] == 'pdf':
                    break
            except:
                pass
        print(os.listdir(temp_loc)[0])
        time.sleep(1)
        temp_file = "temp/{}".format(os.listdir(temp_loc)[0])
        dest_file = "pdfs/{}".format(name)
        os.rename(temp_file, dest_file)

if __name__ == "__main__":
    download_pdf()