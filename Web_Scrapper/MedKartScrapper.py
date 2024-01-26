from bs4 import BeautifulSoup
import re
from selenium import webdriver

'''*********** Creating medkart website scrapper  ***********'''

class Product:
    def __init__(self, link, name, image_url, price, offer_price):
        self.link = link
        self.name = name
        self.image_url = image_url
        self.price = price
        self.offer_price = offer_price

def medkart_url(name):
    url = "https://www.medkart.in/search/all?name="

    modified_name = re.sub(r'[^a-zA-Z0-9\s]+', '', name)
    final_name = modified_name.replace(" ", "%20")
    url += final_name + "/all"
    return url


def medkart_scrapper(driver: webdriver, name):
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
