import requests
from bs4 import BeautifulSoup
import pandas as pd


product_links = []

base_url = 'http://localhost:3000'
current_page = 1
next_page = 2

def getProducts(page):
    url = base_url + "?page=" + str(page)
    response = requests.get(url)

    if response.status_code == 200:

        # Parse de HTML-pagina met BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Vind de links
        links = soup.find_all('a')
    
        #filter de links om enkel degene te nemen met /product_ in de link
        product_links_temp = [link['href'] for link in links if link.has_attr('href') and '/product_' in link['href']]

        #voeg de links toe aan de lijst met product_links
        for link in product_links_temp:
            product_links.append(base_url + link)

        # Vind de link naar de volgende pagina
        next = [link['href'] for link in links if link.has_attr('href') and '/?page' in link['href']]

        # Als er een volgende pagina is, zet de volgende pagina 
        next_page = next[len(next)-1]
    else:
        print('Kon de cataloguspagina niet ophalen. Status code:', response.status_code)

while current_page != next_page + 1:
    getProducts(current_page)
    current_page += 1


# maak een dataframe aan met de kolommen
data_list = []

df = pd.DataFrame(columns=['titel', 'rating', 'descriptie', 'artikel_nummer', 'oude_prijs', 'prijs', 'fotos'])
#CSS selectors BS4
for link in product_links:
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find('h4', {'class': 'product-title'}).text
        rating = 5 - len(soup.find('i', {'class': 'off'}))
        description = soup.find('span', {'class': 'description'}).text
        article_number = soup.find('span', {'class': 'article-number'}).text
        if(soup.find('div', {'class': 'old-price'}) != None):
            old_price = soup.find('div', {'class': 'old-price'}).text
        else:
            old_price = None
        price = soup.find('div', {'class': 'regular-price'}).text
        images = soup.find_all('img', {'class': 'img-fluid'})
        images = list(dict.fromkeys(images))
        image_sources = [base_url + "/" + img['src'] for img in images]

        data_list.append({'titel': title, 'rating': rating, 'descriptie': description, 'artikel_nummer': article_number, 'oude_prijs': old_price, 'prijs': price, 'fotos': image_sources})

df = pd.DataFrame(data_list)   
df.to_csv('BeautifulSoup_CSS_Selectors-products.csv', index=False, encoding='utf-8')

# XPath BS4
from lxml import html

data_list = []

for link in product_links:
    response = requests.get(link)
    if response.status_code == 200:
        
        parsed_html = html.fromstring(response.text)

        #title xpath: /html/body/div[1]/div/div/div/div[2]/div/div[2]/h4
        title = parsed_html.xpath('/html/body/div[1]/div/div/div/div[2]/div/div[2]/h4')[0].text

        #rating parent div xpath: /html/body/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div

        class_name_first_span = parsed_html.xpath('/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div/span[1]/i')[0].get('class')
        rating = 5 - len(parsed_html.xpath('/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div/span[1]/i[@class="' + class_name_first_span + '"]'))

        #description xpath: /html/body/div[1]/div/div/div/div[2]/div/div[2]/span[1]
        description = parsed_html.xpath('/html/body/div[1]/div/div/div/div[2]/div/div[2]/span[1]')[0].text

        #article_number xpath: /html/body/div[1]/div/div/div/div[2]/div/div[2]/span[2]/b
        article_number = parsed_html.xpath('/html/body/div[1]/div/div/div/div[2]/div/div[2]/span[2]/b')[0].text

        #price xpath: /html/body/div[1]/div/div/div/div[2]/div/div[2]/h3/div[1]
        price = parsed_html.xpath('/html/body/div[1]/div/div/div/div[2]/div/div[2]/h3/div[1]/text()[2]')[0]

        #old_price xpath: /html/body/div[1]/div/div/div/div[2]/div/div[2]/h3/div[2]
        old_price = parsed_html.xpath('/html/body/div[1]/div/div/div/div[2]/div/div[2]/h3/div[2]/text()[2]')
        if old_price:
            old_price = old_price[0]
        else:
            old_price = None

        # Gebruik XPath om de img-elementen te selecteren
        image_elements = parsed_html.xpath('//img[contains(@src, "img/products")]')

        # Haal de src-attributen op
        image_sources = [img.get('src') for img in image_elements]

        # verwijder duplicates
        image_sources = list(dict.fromkeys(image_sources))

        #voeg de base_url toe aan de src's
        image_sources = [base_url + "/" + src for src in image_sources]
        
        data_list.append({'titel': title, 'rating': rating, 'descriptie': description, 'artikel_nummer': article_number, 'oude_prijs': old_price, 'prijs': price, 'fotos': image_sources})

df.to_csv('BeautifulSoup_XPath-products.csv', index=False, encoding='utf-8')

# Selenium 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.headless = True
driver = webdriver.Chrome(executable_path='./chromedriver.exe',options=options)

#Selenium CSS selectors
data_list = []

for link in product_links:
    driver.get(link)
    time.sleep(1)

    title = driver.find_element_by_css_selector('h4.product-title').text
    rating = 5 - len(driver.find_elements_by_css_selector('i.off'))
    description = driver.find_element_by_css_selector('span.description').text
    article_number = driver.find_element_by_css_selector('span.article-number').text
    if driver.find_elements_by_css_selector('div.old-price'):
        old_price = driver.find_element_by_css_selector('div.old-price').text
    else:
        old_price = None
    price = driver.find_element_by_css_selector('div.regular-price').text
    images = driver.find_elements_by_css_selector('img.img-fluid')
    image_sources = [img.get_attribute('src') for img in images]
    image_sources = list(dict.fromkeys(image_sources))
    image_sources = [base_url + "/" + src for src in image_sources]
    
    data_list.append({'titel': title, 'rating': rating, 'descriptie': description, 'artikel_nummer': article_number, 'oude_prijs': old_price, 'prijs': price, 'fotos': image_sources})

df.to_csv('Selenium_CSS_Selectors-products.csv', index=False, encoding='utf-8')


# Selenium XPath
data_list = []

for link in product_links:
    driver.get(link)
    time.sleep(1)

    title = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[2]/h4').text
    rating = 5 - len(driver.find_elements_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div/span[1]/i'))
    description = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[2]/span[1]').text
    article_number = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[2]/span[2]/b').text
    if driver.find_elements_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[2]/h3/div[2]'):
        old_price = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[2]/h3/div[2]').text
    else:
        old_price = None
    price = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/div[2]/h3/div[1]').text
    images = driver.find_elements_by_xpath('//img[contains(@src, "img/products")]')
    image_sources = [img.get_attribute('src') for img in images]
    image_sources = list(dict.fromkeys(image_sources))
    image_sources = [base_url + "/" + src for src in image_sources]

    data_list.append({'titel': title, 'rating': rating, 'descriptie': description, 'artikel_nummer': article_number, 'oude_prijs': old_price, 'prijs': price, 'fotos': image_sources})

df.to_csv('Selenium_XPath-products.csv', index=False, encoding='utf-8')


# Scrapy
product_links = []

import scrapy
from scrapy.http import HtmlResponse

class ProductSpider(scrapy.Spider):
    name = 'product_spider'
    start_urls = ['http://localhost:3000']
    overlopen_urls = []

    def parse(self, response):
        # Vind alle productlinks op de huidige pagina
        product_links = response.css('a[href*="/product_"]::attr(href)').extract()
        self.overlopen_urls.append(response.url)

        for link in product_links:
            yield scrapy.Request(url=(base_url + "/" + link), callback=self.parse_product)

        # Ga naar de volgende pagina als die er is ==> als de href van de link bevat /?page=
        page_links = response.css('a[href*="/?page="]::attr(href)').extract()
        for link in page_links:
            link = base_url + "/" + link
            if link not in self.overlopen_urls:
                yield scrapy.Request(link, callback=self.parse)

    def parse_product(self, response):
        # Haal productinformatie van de pagina
        title = response.css('h4.product-title::text').extract_first()
        off_classes = response.css('i.off::attr(class)').extract_first()
        rating = 5 - off_classes.count('off')
        description = response.css('span.description::text').extract_first()
        article_number = response.css('span.article-number::text').extract_first()
        old_price = response.css('div.old-price::text').extract_first()
        price = response.css('div.regular-price::text').extract_first()
        image_sources = [response.urljoin(img) for img in response.css('img.img-fluid::attr(src)').extract()]
        
        #verwijder image duplicates
        image_sources = list(dict.fromkeys(image_sources))


        yield {
            'titel': title,
            'rating': rating,
            'descriptie': description,
            'artikel_nummer': article_number,
            'oude_prijs': old_price,
            'prijs': price,
            'fotos': image_sources
        }

def main():
    # Voer de crawler uit en sla de gegevens op in een CSV-bestand
    df = pd.DataFrame(columns=['titel', 'rating', 'descriptie', 'artikel_nummer', 'oude_prijs', 'prijs', 'fotos'])

    #verwijder oud bestand als die er is
    import os
    if os.path.exists('scrapy-products.csv'):
        os.remove('scrapy-products.csv')

    # Voer de spider uit en sla de resultaten op in een DataFrame
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'scrapy-products.csv',
        'LOG_ENABLED': False
    })

    process.crawl(ProductSpider)
    process.start()

if __name__ == '__main__':
    main()

