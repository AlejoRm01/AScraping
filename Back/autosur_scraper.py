import requests, url_list, json
from bs4 import BeautifulSoup

class AutoSurScraper:
    def __init__(self, base_url, start, increment, max_pag):
        self.base_url = base_url
        self.start = start
        self.increment = increment
        self.max_pag = max_pag

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
                    img_tag = product.find('img')
                    
                    if name_tag and price_tag and img_tag:
                        name = name_tag.text.strip()
                        price = price_tag.text.strip()
                        description = [tag.text.strip() for tag in description_tags]
                        img_url = img_tag.get('src')
                        
                        product_data = {
                            'name': name,
                            'price': price,
                            'description': description,
                            'image_url': img_url
                        }
                        
                        products_list.append(product_data)
        return products_list

    def scrape_all_pages(self):
        urls = []
        for i in range(self.max_pag):
            url = self.base_url.format(self.start + i * self.increment)
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

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

base_url = url_list.autosur_base_url
inicio = 0
incremento = 49
max_paginas = 100

scraper = AutoSurScraper(base_url, inicio, incremento, max_paginas)
products = scraper.scrape_all_pages()

output_filename = 'json/products_autosur.json'
save_to_json(products, output_filename)