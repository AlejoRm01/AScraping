import requests
from bs4 import BeautifulSoup

def get_page_request(url):
    response = requests.get(url) 
    return response

def get_content_autosur(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.find('div', class_='ui-search')
    return content

def get_products_autosur(content):
    products_list = []
    
    products_container = content.find('ol', class_='ui-search-layout ui-search-layout--grid')
    
    for product in products_container:
        
        name = product.find('h2', class_="poly-box").text
        price = product.find('span', class_="andes-money-amount andes-money-amount--cents-superscript").text
        description_tags = product.find_all('li', class_='poly-attributes-list__item poly-attributes-list__bar')
        description = [tag.text for tag in description_tags]
        product_data = {
            'name': name,
            'price': price,
            'description': description
        }
        products_list.append(product_data)
    
    return products_list
    
response = get_page_request('https://vehiculos.mercadolibre.com.co/_Tienda_autosur')

content = get_content_autosur(response)

products = get_products_autosur(content)

for product in products:
    print(f"Nombre: {product['name']}")
    print(f"Precio: {product['price']}")
    print(f"Descripción: {', '.join(product['description'])}")
    print('---')

