from bs4 import BeautifulSoup
import re
from selenium import webdriver


'''*********** Creating indiamart website scrapper  ***********'''

# Creating the object of a medicine
# which includes name, product link, product image, original price and price that offered
class Product:
    def __init__(self, link, name, image_url, price, offer_price):
        self.link = link
        self.name = name
        self.image_url = image_url
        self.price = price
        self.offer_price = offer_price

def indiamart_url(name):
    url = "https://dir.indiamart.com/search.mp?ss="

    modified_name = re.sub(r'[^a-zA-Z0-9\s]+', '', name)
    final_name = url + modified_name.replace(" ", "+")
    return final_name


"""
    # this produces price = -1 --> in case does not find specific price
    # also img_url = "null --> when url is not found
    # it does not have offer prices. Only original prices are available in this site
"""


def indiamart_scrapper(driver: webdriver, name):
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

    for i in range(len(product_link_tags)):
        link = product_link_tags[i]
        name = product_name_tags[i]
        if len(product_image_tags) > i:
            img_url = product_image_tags[i]  # Use ['src'] to get the image URL
        else:
            img_url = "null"
        price = price_tags[i]
        # modifying price formats
        if isinstance(price, str):
            price = re.findall(r'\b\d+\.\d+\b|\b\d+\b', price)
            num = float(price[0])
            price = "{:.2f}".format(num)

        product = Product(link, name, img_url, price, "")
        products.append(product)
    return products
