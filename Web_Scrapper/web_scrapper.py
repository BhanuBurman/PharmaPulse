from bs4 import BeautifulSoup
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')

# Automatically download and manage ChromeDriver
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.opera import OperaDriverManager


def get_driver(browser_name='chrome', headless=True):
    if browser_name.lower() == 'chrome':
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        # Automatically download and manage ChromeDriver
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

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

product_name = "anti dandruff shampoo"


# Creating the object of a medicine
# which includes name, product link, product image, original price and price that offered
class Product:
    def __init__(self, link, name, image_url, price, offer_price):
        self.link = link
        self.name = name
        self.image_url = image_url
        self.price = price
        self.offer_price = offer_price


'''*********** Creating Pharmeasy website scrapper  ***********'''


# returns the url of the pharmeasy website with the given product name
def pharmeasy_url(name):
    url = "https://pharmeasy.in/search/all?name="
    #     remove special characters from the string
    modified_name = re.sub(r'[^a-zA-Z0-9\s]+', '', name)
    final_name = modified_name.replace(" ", "%20")
    url += final_name
    return url


# Scrapper that scraps product information from pharmeasy website
def pharmeasy_scrapper(name):
    product_link = pharmeasy_url(name)

    # get the content of that website
    r = requests.get(product_link)
    htmlContent = r.content
    # print(htmlContent)

    soup = BeautifulSoup(htmlContent, "html.parser")
    # print(soup.prettify())
    # finding product link with the anchor tag of the following class attr
    product_link_tags = soup.find_all("a", {"class": "ProductCard_medicineUnitWrapper__eoLpy ProductCard_defaultWrapper__nxV0R"})
    # finding product names with the h1 tag of the following class attr
    product_names_tags = soup.find_all("h1", {"class": "ProductCard_medicineName__8Ydfq"})  # .text
    # finding product images with the img tag of the following class attr
    product_image_tags = soup.find_all("img", {"class": "ProductCard_productImage__dq5lq"})  # ["src"]

    # this section a bit confusing...
    # here we have to find prices and offered prices but in some of the cases the prices may not be given so we
    # cannot directly the price or offered price class rather we target their parent class
    price_tags = soup.find_all("div", {"class": "ProductCard_priceContainer__dqj7Q"})

    # container that stores all the objects of the medicines
    products = []

    # Iterating through all the products within the web page
    for i in range(len(product_names_tags)):
        link = "https://pharmeasy.in/" + product_link_tags[i]["href"]
        name = product_names_tags[i].text
        img_url = product_image_tags[i].get('src')  # Use ['src'] to get the image URL

        price_tag = price_tags[i]  # Get the specific price tag for this product

        # initially make price and offer price empty string
        price = ""
        offer = ""

        # use descendants to recursively iterate all the children of the given tag
        for child in price_tag.descendants:
            if child.name:
                child_class = child.get('class')
                # this is original price that has been crossed
                if child_class and child_class[0] == "ProductCard_striked__jkSiD":
                    price = child.get_text(strip=True)
                # offer price with coupon
                elif child_class and child_class[0] == "ProductCard_gcdDiscountContainer__CCi51":
                    offer = child.get_text(strip=True)
                # general offer price
                elif child_class and child_class[0] == "ProductCard_ourPrice__yDytt":
                    offer = child.get_text(strip=True)

        # modifying price formats
        price = re.findall(r'\b\d+\.\d+\b|\b\d+\b', price)
        offer = re.findall(r'\b\d+\.\d+\b|\b\d+\b', offer)
        if len(price) == 1:
            price = price[0]
            offer = float(offer[0])
            offer = "{:.2f}".format(offer)
        elif len(offer) == 1:
            price = offer[0]
            offer = ""

        product = Product(link, name, img_url, price, offer)
        products.append(product)
    return products


'''*********** Creating Netmeds website scrapper  ***********'''


def netmeds_url(name):
    url = "https://www.netmeds.com/catalogsearch/result/"

    modified_name = re.sub(r'[^a-zA-Z0-9\s]+', '', name)
    final_name = modified_name.replace(" ", "%20")
    url += final_name + "/all"
    # print(url)
    return url


def netmeds_scrapper(name):
    product_link = netmeds_url(name)

    driver.get(product_link)

    # Allow some time for the page to load before attempting to fetch the elements
    driver.implicitly_wait(10)  # Adjust the waiting time if necessary

    # get the content of that website
    htmlContent = driver.page_source
    # print(htmlContent)

    soup = BeautifulSoup(htmlContent, "html.parser")
    # print(soup.prettify())
    products = []
    product_link_tags = soup.find_all("a", {"class": "category_name"})
    product_names = soup.find_all("span", {"class": "clsgetname"})
    product_image_tags = soup.find_all("img", {"class": "product-image-photo"})  # ["src"]

    # this section a bit confusing...
    # here we have to find prices and offered prices but in some of the cases the prices may not be given so we
    # cannot directly the price or offered price class rather we target their parent class
    price_tags = soup.find_all("span", {"class": "price-box"})

    for i in range(len(product_link_tags)):
        link = "https://www.netmeds.com/" + product_link_tags[i]["href"]
        name = product_names[i].text
        img_url = product_image_tags[i].get('src')  # Use ['src'] to get the image URL
        price_tag = price_tags[i]
        # initially make price and offer price empty string
        price = ""
        offer = ""

        for child in price_tag.descendants:
            if child.name:
                child_class = child.get('class')
                # this is original price that has been crossed
                if child_class and child_class[0] == "price":
                    price = child.get_text(strip=True)
                # offer price with coupon
                elif child_class and child_class[0] == "final-price":
                    offer = child.get_text(strip=True)
                # general offer price
                else:
                    child_id = child.get('id')
                    if child_id and child_id == "final_price":
                        price = child.get_text(strip=True)
        # modifying price formats
        price = re.findall(r'\b\d+\.\d+\b|\b\d+\b', price)
        offer = re.findall(r'\b\d+\.\d+\b|\b\d+\b', offer)
        if len(offer) != 0:
            price = price[0]
            offer = float(offer[0])
            offer = "{:.2f}".format(offer)
        else:
            price = price[0]
        product = Product(link, name, img_url, price, offer)
        products.append(product)
    return products


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


'''*********** Creating medkart website scrapper  ***********'''


def medkart_url(name):
    url = "https://www.medkart.in/search/all?name="

    modified_name = re.sub(r'[^a-zA-Z0-9\s]+', '', name)
    final_name = modified_name.replace(" ", "%20")
    url += final_name + "/all"
    print(url)
    return url


def medkart_scrapper(name):
    product_link = medkart_url(name)
    # get the content of that website
    driver.get(product_link)

    # Allow some time for the page to load before attempting to fetch the elements
    driver.implicitly_wait(10)  # Adjust the waiting time if necessary

    # get the content of that website
    htmlContent = driver.page_source

    soup = BeautifulSoup(htmlContent, "html.parser", multi_valued_attributes=None)
    products = []
    product_link_tags = soup.find_all("a", {"class": "col-lg-8 col-8 p-0"})
    product_names = soup.find_all("div", {"class": "ListingCard_med_mobile_info__qjA38"})  # .h3.text
    product_image_tags = soup.find_all("div", {"class": "row justify-content-center"})  # .img["src"]
    price_tags = soup.find_all("div", {"class": "flex-center-center pricing mt-3 ps-0 ListingCard_pricing_mobile__U9wGi"})

    for i in range(len(product_link_tags)):
        link = "https://www.netmeds.com/" + product_link_tags[i]["href"]
        name = product_names[i].h3.text
        img_url = product_image_tags[i].noscript.img['src']  # Use ['src'] to get the image URL
        original = price_tags[i].h4.text
        offer = price_tags[i].h3.text

        # modifying price formats
        price = re.findall(r'\b\d+\.\d+\b|\b\d+\b', original)
        offer = re.findall(r'\b\d+\.\d+\b|\b\d+\b', offer)
        if len(offer) != 0:
            price = price[0]
            offer = float(offer[0])
            offer = "{:.2f}".format(offer)
        else:
            price = price[0]
        product = Product(link, name, img_url, price, offer)
        products.append(product)
    # print(product_names)
    return products


'''*********** Creating indiamart website scrapper  ***********'''


def indiamart_url(name):
    url = "https://dir.indiamart.com/search.mp?ss="

    modified_name = re.sub(r'[^a-zA-Z0-9\s]+', '', name)
    final_name = url + modified_name.replace(" ", "+")
    print(final_name)
    return final_name


"""
    # this produces price = -1 --> in case does not find specific price
    # also img_url = "null --> when url is not found
    # it does not have offer prices. Only original prices are available in this site
"""


def indiamart_scrapper(name):
    product_link = indiamart_url(name)
    # get the content of that website
    driver.get(product_link)

    # Allow some time for the page to load before attempting to fetch the elements
    driver.implicitly_wait(10)  # Adjust the waiting time if necessary

    # get the content of that website
    htmlContent = driver.page_source

    soup = BeautifulSoup(htmlContent, "html.parser", multi_valued_attributes=None)
    products = []
    list = soup.find_all("div", {"class": "prd-top df flx100 oh"})  # .text
    product_link_tags = []
    product_name_tags = []
    product_image_tags = []  # .img["src"]
    # product_image_tags =soup.find_all("div", {"class": "prd-list imgc w100"}) # .img["src"]
    price_tags = []
    # for counting the indexes
    count = 0;
    for ele in list:

        for child in ele.descendants:
            if child.name:
                child_class = child.get('class')
                # this is original price that has been crossed
                if child_class and (child_class == "prd-list-name pn-trgt flx100" or child_class == "prd-list-name flx100 grdprdName"):

                    link_tag = child.span.a
                    if link_tag:
                        link = link_tag['href'].split(" ")
                        item_name = link_tag.text
                        product_link_tags.append(link[0])
                        product_name_tags.append(item_name)
                    else:
                        # Handle the case where 'a' tag is not present
                        print("No 'a' tag found for product name.")
                # offer price with coupon
                elif child_class and (child_class == "prd-list-prc flx100 tac" or child_class == "prd-list-prc flx100 tac grdprctyp"):
                    if child.span.span is not None:
                        price_tags.append(child.span.span.get_text(strip=True))
                    else:
                        # assigning the None values as -1
                        price_tags.append(-1)
                        # to show the None indexes
                        # print("Count No.", count)
                # general offer price
                elif child_class and child_class == "prd-list imgc w100":
                    if child.img:
                        product_image_tags.append(child.img['src'])
                    else:
                        # Handle the case where 'img' tag is not present
                        product_image_tags.append("null")
                        print("No 'img' tag found for product image.")
    #
    # print(product_link_tags)
    # print(product_image_tags)
    print(len(price_tags))
    print(len(product_link_tags))
    print(len(product_image_tags))
    # print(list)
    # print(list[2])

    # for i in range(len(product_link_tags)):

    for i in range(len(product_link_tags)):
        link = product_link_tags[i]
        name = product_name_tags[i]
        if len(product_image_tags) > i:
            img_url = product_image_tags[i]  # Use ['src'] to get the image URL
        else:
            img_url = "null"
        price = price_tags[i]
        # print(type(price))
        # modifying price formats
        if isinstance(price, str):
            price = re.findall(r'\b\d+\.\d+\b|\b\d+\b', price)
            num = float(price[0])
            price = "{:.2f}".format(num)

        product = Product(link, name, img_url, price, "")
        products.append(product)
    return products


'''*********** Creating TATA 1mg website scrapper  ***********'''


# returns the url of the pharmeasy website with the given product name
def tata_mg_url(name):
    url = "https://www.1mg.com/search/all?name="
    #     remove special characters from the string
    modified_name = re.sub(r'[^a-zA-Z0-9\s]+', '', name)
    final_name = modified_name.replace(" ", "%20")
    url += final_name
    print(url)
    return url


# Scrapper that scraps product information from TATA 1mg website
def tata_mg_scrapper(name):
    product_link = tata_mg_url(name)
    # get the content of that website
    driver.get(product_link)

    # Allow some time for the page to load before attempting to fetch the elements
    driver.implicitly_wait(10)  # Adjust the waiting time if necessary

    # get the content of that website
    htmlContent = driver.page_source
    # print(htmlContent)
    soup = BeautifulSoup(htmlContent, "html.parser", multi_valued_attributes=None)
    # print(soup.prettify())
    products = []
    product_link_tags = soup.find_all("a", {"class": "style__product-link___1hWpa"})
    product_names = soup.find_all("div", {"class": "style__pro-title___3G3rr"})  # .h3.text

    # in this website due to dynamic loading the images are not being loaded
    # Only three images can be loaded
    product_image_tags = soup.find_all("img", {"class": "style__image___Ny-Sa style__loaded___22epL"})
    # product_image_tags = soup.find_all("img", {"class": "style__product-image___1bkgA"})  # .img["src"] style__image___Ny-Sa style__loaded___22epL

    price_tags = soup.find_all("div", {"class": "style__product-pricing___1OxnE"})
    # print(len(product_link_tags))
    # print(len(product_names))
    # print(len(product_image_tags))
    # print(len(price_tags))
    # print(product_link_tags[2].img)

    #
    for i in range(len(product_link_tags)):
        link = "https://www.1mg.com/" + product_link_tags[i]['href']
        name = product_names[i].text
        # if i < len(product_image_tags) and product_image_tags[i].div.img != None:
        #     img_url = product_image_tags[i].div.img['src']
        # else:
        #     img_url = "null"
        if i < len(product_image_tags):
            img_url = product_image_tags[i]['src']
        else:
            img_url = "null"

        price_tag = price_tags[i].div
        price = ""
        offer = ""

        # Check for the first structure
        discount_price_tag = price_tag.find("span", {"class": "style__discount-price___qlNIB"})
        if discount_price_tag:
            price = discount_price_tag.get_text(strip=True)

        # Check for the second structure if the first one didn't find the price
        if not price:
            price_tag_large_mrp = price_tag.find("span", {"class": "style__mrp-tag___p4Shc style__large___3wbE4"})
            if price_tag_large_mrp:
                price = price_tag.get_text(strip=True).replace(price_tag_large_mrp.get_text(strip=True), "")

        # Check for offer price
        offer_tag = price_tag.find("div", {"class": "style__price-tag___KzOkY"})
        if offer_tag:
            offer = offer_tag.get_text(strip=True)

        # print("Original Price:", price)
        # print("Offer Price:", offer)
        # # modifying price formats
        price = re.findall(r'\b\d+\.\d+\b|\b\d+\b', price)
        offer = re.findall(r'\b\d+\.\d+\b|\b\d+\b', offer)
        # print(price)
        # print(offer)
        if len(offer) != 0:
            offer = float(offer[0])
            offer = "{:.2f}".format(offer)
        if len(price) != 0:
            price = float(price[0])
            price = "{:.2f}".format(price)

        product = Product(link, name, img_url, price, offer)
        products.append(product)
    # print(product_names)
    return products


# my_products = indiamart_scrapper(product_name)
# my_products = pharmeasy_scrapper(product_name)
# my_products2 = netmeds_scrapper(product_name)
# print_products(my_products)

# tata_mg_scrapper(product_name)
my_products3 = tata_mg_scrapper(product_name)
print_products(my_products3)
# #
# print_products(my_products3)
# print(my_products[0].price)
# print(my_products[1].price)
# print(my_products[2].price)
