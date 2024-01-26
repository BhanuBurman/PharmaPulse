from bs4 import BeautifulSoup
import re
from selenium import webdriver

'''*********** Creating TATA 1mg website scrapper  ***********'''


# Creating the object of a medicine
# which includes name, product link, product image, original price and price that offered
class Product:
    def __init__(self, link, name, image_url, price, offer_price):
        self.link = link
        self.name = name
        self.image_url = image_url
        self.price = price
        self.offer_price = offer_price

# returns the url of the pharmeasy website with the given product name
def tata_mg_url(name):
    url = "https://www.1mg.com/search/all?name="
    #     remove special characters from the string
    modified_name = re.sub(r'[^a-zA-Z0-9\s]+', '', name)
    final_name = modified_name.replace(" ", "%20")
    url += final_name
    return url


# Scrapper that scraps product information from TATA 1mg website
def tata_mg_scrapper(driver: webdriver, name):
    product_link = tata_mg_url(name)
    # get the content of that website
    driver.get(product_link)

    # Allow some time for the page to load before attempting to fetch the elements
    driver.implicitly_wait(10)  # Adjust the waiting time if necessary

    # get the content of that website
    htmlContent = driver.page_source
    soup = BeautifulSoup(htmlContent, "html.parser", multi_valued_attributes=None)
    products = []
    product_link_tags = soup.find_all("a", {"class": "style__product-link___1hWpa"})
    product_names = soup.find_all("div", {"class": "style__pro-title___3G3rr"})  # .h3.text

    # in this website due to dynamic loading the images are not being loaded
    # Only three images can be loaded
    product_image_tags = soup.find_all("img", {"class": "style__image___Ny-Sa style__loaded___22epL"})

    price_tags = soup.find_all("div", {"class": "style__product-pricing___1OxnE"})

    for i in range(len(product_link_tags)):
        link = "https://www.1mg.com/" + product_link_tags[i]['href']
        name = product_names[i].text

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

        # # modifying price formats
        price = re.findall(r'\b\d+\.\d+\b|\b\d+\b', price)
        offer = re.findall(r'\b\d+\.\d+\b|\b\d+\b', offer)

        if len(offer) != 0:
            offer = float(offer[0])
            offer = "{:.2f}".format(offer)
        if len(price) != 0:
            price = float(price[0])
            price = "{:.2f}".format(price)

        product = Product(link, name, img_url, price, offer)
        products.append(product)

    return products
