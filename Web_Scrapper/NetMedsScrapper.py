from bs4 import BeautifulSoup
import re
import requests
from selenium import webdriver

"""*********** Creating Netmeds website scrapper  ***********"""

# Creating the object of a medicine
# which includes name, product link, product image, original price and price that offered
class Product:
    def __init__(self, link, name, image_url, price, offer_price):
        self.link = link
        self.name = name
        self.image_url = image_url
        self.price = price
        self.offer_price = offer_price




def netmeds_url(name):
    url = "https://www.netmeds.com/catalogsearch/result/"

    modified_name = re.sub(r'[^a-zA-Z0-9\s]+', '', name)
    final_name = modified_name.replace(" ", "%20")
    url += final_name + "/all"
    # print(url)
    return url


def netmeds_scrapper(driver: webdriver, name):
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
