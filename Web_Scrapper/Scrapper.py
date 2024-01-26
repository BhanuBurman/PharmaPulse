from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

import os
import sys

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory to the Python path
parent_dir = os.path.join(current_dir, 'Web_Scrapper')
sys.path.append(parent_dir)

from .PharmEasyScrapper import pharmeasy_scrapper
from .NetMedsScrapper import netmeds_scrapper
from .MedKartScrapper import medkart_scrapper
from .TATA1mgScrapper import tata_mg_scrapper
from .IndiaMartScrapper import indiamart_scrapper

from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.opera import OperaDriverManager

# """Enter the Product Name Here : """
# product_name = "anti dandruff shampoo"


def get_driver(browser_name='chrome', headless=True):
    if browser_name.lower() == 'chrome':
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        # Automatically download and manage ChromeDriver
        # return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        return webdriver.Chrome(service=Service(), options=options)

    elif browser_name.lower() == 'firefox':
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

    elif browser_name.lower() == 'safari':
        # Safari doesn't support headless mode
        return webdriver.Safari()

    elif browser_name.lower() == 'edge':
        options = webdriver.EdgeOptions()
        if headless:
            raise ValueError("Edge does not support headless mode.")
        return webdriver.Edge(service=EdgeChromiumDriverManager().install(), options=options)

    elif browser_name.lower() == 'opera':
        options = webdriver.ChromeOptions()
        if headless:
            raise ValueError("Opera does not support headless mode.")
        return webdriver.Chrome(service=OperaDriverManager().install(), options=options)

    elif browser_name.lower() == 'brave':
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.binary_location = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'  # Update the path
        return webdriver.Chrome(service=ChromeDriverManager().install(), options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser_name}")


# Usage:
browser = 'chrome'  # or 'firefox', 'edge', etc.
headless_mode = True  # or False for non-headless mode

driver = get_driver(browser, headless_mode)

def print_products(my_products):
    count = 1
    for product in my_products:
        print("Medicine No. ", count)
        print("Link : ", product.link)
        print("Name : ", product.name)
        if "base64" in product.image_url:
            print("Image Url not found...")
        else:
            print("Image Url : ", product.image_url)
        # print("Url type : ",type(product.image_url))
        print("original price : ", product.price, "Rs")
        # print("original price type: ",type(product.price))
        print("offer price : ", product.offer_price if len(product.offer_price) > 0 else "No any offer", "Rs")
        print("----------------------------------------------")
        count += 1

def search_products(product_name):
    my_products1 = pharmeasy_scrapper(product_name)
    my_products2 = netmeds_scrapper(driver, product_name)
    my_products3 = medkart_scrapper(driver, product_name)
    my_products4 = indiamart_scrapper(driver, product_name)
    my_products5 = tata_mg_scrapper(driver, product_name)

    final_product_list  = [my_products1,my_products2,my_products3,my_products4,my_products5]


    return final_product_list


# final_product_list  = search_products("cough syrup")
# print("PharmEasy Website Products ---->")
# print_products(final_product_list[0])
# print("\n\n")
# print("NetMeds Website Products ---->")
# print_products(final_product_list[1])
# print("\n\n")
# print("MedKart Website Products ---->")
# print_products(final_product_list[2])
# print("\n\n")
# print("IndiaMart Website Products ---->")
# print_products(final_product_list[3])
# print("\n\n")
# print("TATA 1mg Website Products ---->")
# print_products(final_product_list[4])

# print(len(final_product_list[0]))
# print(len(final_product_list[1]))
# print(len(final_product_list[2]))
# print(len(final_product_list[3]))
# print(len(final_product_list[4]))
