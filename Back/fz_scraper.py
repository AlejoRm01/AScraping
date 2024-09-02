import requests, url_list, json, time
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc

def get_page_content(url):
    browser = uc.Chrome()
    browser.get(url)
    browser.implicitly_wait(1000)
    
    page_source = browser.page_source 
    browser.close()
    browser.quit()
    
    soup = BeautifulSoup(page_source, 'html.parser')
    content = soup.find('div', class_='col-12 col-md-9')
    
    return content

def get_products_fz(content):
    product_list = []
    if content:
        products_container = content.find('div', class_='row justify-around')
        if products_container:
            for product in products_container.find_all('div', recursive=False):
                # Extraer el nombre del producto
                name_tag = product.find('div', class_="title-font")
                name = name_tag.text.strip() if name_tag else 'N/A'
                
                # Extraer el precio del producto
                price_tag = product.find('div', class_="avenir-bold")
                price = price_tag.text.strip() if price_tag else 'N/A'
                
                # Extraer la URL de la imagen del producto
                img_tag = product.find('div', class_="q-carousel__slide")
                img_url = img_tag['style'].split('url("')[1].split('")')[0] if img_tag else 'N/A'
                
                # Extraer la descripción (año, kilometraje, motor)
                details_tags = product.find_all('div', class_="q-mr-sm")
                year = details_tags[0].text.strip() if len(details_tags) > 0 else 'N/A'
                km = details_tags[1].text.strip() if len(details_tags) > 1 else 'N/A'
                motor = details_tags[2].text.strip() if len(details_tags) > 2 else 'N/A'

                product_data = {
                    'name': name,
                    'price': price,
                    'image_url': img_url,
                    'year': year,
                    'kilometraje': km,
                    'motor': motor
                }
                product_list.append(product_data)
    
    return product_list

base_url = url_list.fzautos_base_url

content = get_page_content(base_url)

products = get_products_fz(content)
print(products)
output_filename = 'json/products_fzautos.json'