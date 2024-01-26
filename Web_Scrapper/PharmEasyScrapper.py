from bs4 import BeautifulSoup
import re
import requests



# Creating the object of a medicine
# which includes name, product link, product image, original price and price that offered
class Product:
    def __init__(self, link, name, image_url, price, offer_price):
        self.link = link
        self.name = name
        self.image_url = image_url
        self.price = price
        self.offer_price = offer_price


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

    r = requests.get(product_link)
    htmlContent = r.content

    soup = BeautifulSoup(htmlContent, "html.parser")
    # print(soup.prettify())
    # finding product link with the anchor tag of the following class attr
    product_link_tags = soup.find_all("a", {"class": "ProductCard_medicineUnitWrapper__eoLpy ProductCard_defaultWrapper__nxV0R"})
    # finding product names with the h1 tag of the following class attr
    product_names_tags = soup.find_all("h1", {"class": "ProductCard_medicineName__8Ydfq"})  # .text
    # finding product images with the img tag of the following class attr
    product_image_tags = soup.find_all("div", {"class": "ProductCard_medicineImgDefault__Q8XbJ"})  # ["src"]

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
        img_url = product_image_tags[i].noscript.img['src']  # Use ['src'] to get the image URL

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
