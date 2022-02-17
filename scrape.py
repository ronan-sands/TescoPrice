from bs4 import BeautifulSoup
import requests
import re
import math
from datetime import datetime
import json
from lxml import html
from fake_useragent import UserAgent

now = datetime.now()
time = now.strftime("%H:%M:%S")
print("Started at {}".format(time))
ua = UserAgent()
print(ua.chrome)
headers = {'User-Agent':str(ua.safari)}
class Product:
    def __init__(self, id, title, category, price, img_src):
        self.id = id
        self.title = title
        self.category = category
        self.price = price
        self.img_src = img_src
    def to_dict(self):
      return {"id": self.id, "title": self.title, "category": self.category, "price": self.price, "img_src": self.img_src}

def productToJsonObject(product):
    return json.dumps(product.__dict__)

def productsToJsonArray(products):
    productList = [prod.to_dict() for prod in products]
    productData = json.dumps({"products" : productList})
    return productData


def getProductsFromTiles(product_tiles, category):
    product_list = []
    for product in product_tiles:
        try:
            prod_id = product.get('data-auto-id')
            match = product.find('div', class_='product-details--content')
            name = match.find('a').text
            spanprice = product.find('span', class_= 'value')
            txtprice = spanprice.text.strip()
            price = float(txtprice)
            img_tag = product.find('img', class_='product-image')
            img_src = img_tag.get('src')
            prod = Product(prod_id, name, category, price, img_src)
            product_list.append(prod)            
        except Exception as e:
            print(e)
            pass
    return product_list

def getNumPages(soup):
    num_items_div = soup.find('div', class_='pagination__items-displayed')
    num_items_div_text = num_items_div.text
    num_items_text = re.search('of (.*) item', num_items_div_text)
    num_items = int(num_items_text.group(1))
    num_pages = math.ceil(num_items/24)
    return num_pages



def getProductsFromCategory(category):
    url = 'https://www.tesco.com/groceries/en-GB/shop/{}/all'.format(category)
    product_list = []
    try:
        source = requests.get(url, headers=headers, timeout=5).text
        
        soup = BeautifulSoup(source, 'lxml')
        num_pages = getNumPages(soup)    
        product_tiles = soup.find_all('div', class_='tile-content')
        product_list = product_list + (getProductsFromTiles(product_tiles, category))
        i = range(2, num_pages + 1)
        for x in i:
            source = requests.get('{}?page={}'.format(url, x), headers=headers).text
            soup = BeautifulSoup(source, 'lxml')
            product_tiles = soup.find_all('div', class_='tile-content')
            product_list = product_list + (getProductsFromTiles(product_tiles, category))
    except Exception as e:
        print(e)
        pass
    return product_list

def getProductsFromSearch(query):
    url = 'https://www.tesco.com/groceries/en-GB/search?query={}'.format(query)
    product_list = []
    try:
        source = requests.get(url, headers=headers, timeout=5).text
        soup = BeautifulSoup(source, 'lxml')
        num_pages = getNumPages(soup)    
        product_tiles = soup.find_all('div', class_='tile-content')
        product_list = product_list + (getProductsFromTiles(product_tiles, 'Searched Item'))
        i = range(2, num_pages + 1)
        for x in i:
            source = requests.get('{}?page={}'.format(url, x), headers=headers).text
            soup = BeautifulSoup(source, 'lxml')
            product_tiles = soup.find_all('div', class_='tile-content')
            product_list = product_list + (getProductsFromTiles(product_tiles, 'Searched Item'))
    except Exception as e:
        pass
    return product_list

def getProductById(id):
    url = 'https://www.tesco.com/groceries/en-GB/products/{}'.format(id)
    try:
        source = requests.get(url, headers=headers, timeout=5).text
        soup = BeautifulSoup(source, 'lxml')
        doc = html.fromstring(source)
        return [getProductFromWebPage(id, soup, doc)]
    except Exception as e:
        print(e)

def getProductFromWebPage(id, soup, parsed):
    title = soup.find('h1', class_='product-details-tile__title').text
    try:
        category = parsed.xpath('/html/body/div[1]/div/div/div[3]/div[1]/div/div[1]/div[1]/div/nav/ol/li[2]/div/a/span')[0].text
    except:
        category = 'Unknown'
    price_str = soup.find('span', class_='value').text
    price = float(price_str)
    img_tag = soup.find('img', class_='product-image')
    img_src = img_tag.get('src')
    product = Product(id, title, category, price, img_src)
    return product
