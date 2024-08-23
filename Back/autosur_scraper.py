import requests, url_list
from bs4 import BeautifulSoup

class AutoSurScraper:
    def __init__(self, base_url, inicio, incremento, max_paginas):
        self.base_url = base_url
        self.inicio = inicio
        self.incremento = incremento
        self.max_paginas = max_paginas

    def get_page_request(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Error al solicitar la página: {e}")
            return None

    def get_content_autosur(self, response):
        if response:
            soup = BeautifulSoup(response.content, 'html.parser')
            content = soup.find('div', class_='ui-search')
            return content
        return None

    def get_products_autosur(self, content):
        products_list = []
        if content:
            products_container = content.find('ol', class_='ui-search-layout ui-search-layout--grid')
            if products_container:
                for product in products_container.find_all('li'):
                    name_tag = product.find('h2', class_="poly-box")
                    price_tag = product.find('span', class_="andes-money-amount andes-money-amount--cents-superscript")
                    description_tags = product.find_all('li', class_='poly-attributes-list__item poly-attributes-list__bar')

                    if name_tag and price_tag:
                        name = name_tag.text.strip()
                        price = price_tag.text.strip()
                        description = [tag.text.strip() for tag in description_tags]

                        product_data = {
                            'name': name,
                            'price': price,
                            'description': description
                        }
                        products_list.append(product_data)
        return products_list

    def scrape_all_pages(self):
        urls = []
        for i in range(self.max_paginas):
            url = self.base_url.format(self.inicio + i * self.incremento)
            response = self.get_page_request(url)
            if response and response.status_code == 200:
                content = self.get_content_autosur(response)
                if content:
                    products = self.get_products_autosur(content)
                    if products:
                        urls.append((url, products))
                    else:
                        print(f"No se encontraron productos en: {url}")
                        break
                else:
                    print(f"No se pudo obtener el contenido de la página: {url}")
                    break
            else:
                print(f"Error al acceder a la página: {url}")
                break
        return urls

base_url = url_list.autosur_base_url
inicio = 49
incremento = 48
max_paginas = 100

scraper = AutoSurScraper(base_url, inicio, incremento, max_paginas)
page_data = scraper.scrape_all_pages()

for url, products in page_data:
    print(f"Productos de la página: {url}")
    for product in products:
        print(f"Nombre: {product['name']}")
        print(f"Precio: {product['price']}")
        print(f"Descripción: {', '.join(product['description'])}")
        print('---')