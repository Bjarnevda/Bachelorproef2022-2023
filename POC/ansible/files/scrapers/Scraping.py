import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import sys


port = sys.argv[1]

base_url = "http://localhost:" + port

product_links = []

current_page = 1
next_page = 2

if os.path.exists("BeautifulSoup_CSS_Selectors-products_" + port + ".csv"):
    os.remove("BeautifulSoup_CSS_Selectors-products_" + port + ".csv")

if os.path.exists("BeautifulSoup_XPath-products_" + port + ".csv"):
    os.remove("BeautifulSoup_XPath-products_" + port + ".csv")

if os.path.exists("Selenium_CSS_Selectors-products_" + port + ".csv"):
    os.remove("Selenium_CSS_Selectors-products_" + port + ".csv")

if os.path.exists("Selenium_XPath-products_" + port + ".csv"):
    os.remove("Selenium_XPath-products_" + port + ".csv")

if os.path.exists("scrapy-products_" + port + ".csv"):
    os.remove("scrapy-products_" + port + ".csv")


def getProducts(page):
    url = base_url + "?page=" + str(page)
    response = requests.get(url)

    if response.status_code == 200:
        # Parse de HTML-pagina met BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Vind de links
        links = soup.find_all("a")

        # filter de links om enkel degene te nemen met /product_ in de link
        product_links_temp = [
            link["href"]
            for link in links
            if link.has_attr("href") and "/product_" in link["href"]
        ]

        # voeg de links toe aan de lijst met product_links
        for link in product_links_temp:
            product_links.append(base_url + link)

        # Vind de link naar de volgende pagina
        next = [
            link["href"]
            for link in links
            if link.has_attr("href") and "/?page" in link["href"]
        ]

        # Als er een volgende pagina is, zet de volgende pagina
        next_page = next[len(next) - 1]
    else:
        print("Kon de cataloguspagina niet ophalen. Status code:", response.status_code)


while current_page != next_page + 1:
    getProducts(current_page)
    current_page += 1


# maak een dataframe aan met de kolommen
data_list = []

df = pd.DataFrame(
    columns=[
        "titel",
        "rating",
        "descriptie",
        "artikel_nummer",
        "oude_prijs",
        "prijs",
        "fotos",
        "status_code",
        "page_load_time",
    ]
)
# CSS selectors BS4

for link in product_links:
    response = requests.get(link)

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        title = soup.find("h4", {"class": "product-title"}).text
    except AttributeError:
        title = None
    try:
        rating = 5 - len(soup.find("i", {"class": "off"}))
    except (AttributeError, TypeError):
        rating = None
    try:
        description = soup.find("span", {"class": "description"}).text
    except AttributeError:
        description = None
    try:
        article_number = soup.find("span", {"class": "article-number"}).text
    except AttributeError:
        article_number = None
    try:
        old_price = soup.find("div", {"class": "old-price"}).text
    except AttributeError:
        old_price = None
    try:
        price = soup.find("div", {"class": "regular-price"}).text
    except AttributeError:
        price = None
    try:
        images = soup.find_all("img", {"class": "img-fluid"})
    except AttributeError:
        images = []
    images = list(dict.fromkeys(images))
    image_sources = [base_url + "/" + img["src"] for img in images]
    data_list.append(
        {
            "titel": title,
            "rating": rating,
            "descriptie": description,
            "artikel_nummer": article_number,
            "oude_prijs": old_price,
            "prijs": price,
            "fotos": image_sources,
            "status_code": response.status_code,
            "page_load_time": None,
        }
    )

df = pd.DataFrame(data_list)
df.to_csv(
    "BeautifulSoup_CSS_Selectors-products_" + port + ".csv",
    index=False,
    encoding="utf-8",
)

# XPath BS4
from lxml import html

data_list = []

for link in product_links:
    response = requests.get(link)
    parsed_html = html.fromstring(response.text)
    try:
        title_element = parsed_html.xpath(
            "/html/body/div[1]/div/div/div/div[2]/div/div[2]/h4"
        )[0]
        title = title_element.text
    except (IndexError, AttributeError):
        title = None
    try:
        class_name_first_span = parsed_html.xpath(
            "/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div/span[1]/i"
        )[0].get("class")
        rating_elements = parsed_html.xpath(
            '/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div/span[1]/i[@class="'
            + class_name_first_span
            + '"]'
        )
        rating = 5 - len(rating_elements)
    except (IndexError, AttributeError):
        rating = None
    try:
        description_element = parsed_html.xpath(
            "/html/body/div[1]/div/div/div/div[2]/div/div[2]/span[1]"
        )[0]
        description = description_element.text
    except (IndexError, AttributeError):
        description = None
    try:
        article_number_element = parsed_html.xpath(
            "/html/body/div[1]/div/div/div/div[2]/div/div[2]/span[2]/b"
        )[0]
        article_number = article_number_element.text
    except (IndexError, AttributeError):
        article_number = None
    try:
        price_element = parsed_html.xpath(
            "/html/body/div[1]/div/div/div/div[2]/div/div[2]/h3/div[1]/text()[2]"
        )[0]
        price = price_element
    except (IndexError, AttributeError):
        price = None
    try:
        old_price_element = parsed_html.xpath(
            "/html/body/div[1]/div/div/div/div[2]/div/div[2]/h3/div[2]/text()[2]"
        )
        old_price = old_price_element[0] if old_price_element else None
    except (IndexError, AttributeError):
        old_price = None
    try:
        image_elements = parsed_html.xpath('//img[contains(@src, "img/products")]')
    except (IndexError, AttributeError):
        image_elements = []
    # Haal de src-attributen op
    image_sources = [img.get("src") for img in image_elements]
    # verwijder duplicates
    image_sources = list(dict.fromkeys(image_sources))
    # voeg de base_url toe aan de src's
    image_sources = [base_url + "/" + src for src in image_sources]
    data_list.append(
        {
            "titel": title,
            "rating": rating,
            "descriptie": description,
            "artikel_nummer": article_number,
            "oude_prijs": old_price,
            "prijs": price,
            "fotos": image_sources,
            "status_code": response.status_code,
            "page_load_time": None,
        }
    )

df = pd.DataFrame(data_list)
df.to_csv(
    "BeautifulSoup_XPath-products_" + port + ".csv", index=False, encoding="utf-8"
)

# Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.headless = True
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

# Selenium CSS selectors
data_list = []

for link in product_links:
    start_time = time.time()
    driver.get(link)
    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
    custom_js_locator = (By.XPATH, "//script[@src='js/custom.js']")
    wait.until(EC.presence_of_element_located(custom_js_locator))
    end_time = time.time()
    page_load_time = end_time - start_time
    response = driver.execute_async_script(
        "var callback = arguments[arguments.length - 1]; fetch('"
        + link
        + "').then((response) => response.text().then((text) => callback({'status': response.status, 'text': text})))"
    )

    status_code = response["status"]
    try:
        title = driver.find_element(by=By.CSS_SELECTOR, value="h4.product-title").text
    except NoSuchElementException:
        title = None

    try:
        rating = 5 - len(driver.find_elements(by=By.CSS_SELECTOR, value="i.off"))
    except NoSuchElementException:
        rating = None

    try:
        description = driver.find_element(
            by=By.CSS_SELECTOR, value="span.description"
        ).text
    except NoSuchElementException:
        description = None

    try:
        article_number = driver.find_element(
            by=By.CSS_SELECTOR, value="span.article-number"
        ).text
    except NoSuchElementException:
        article_number = None

    try:
        old_price_element = driver.find_element(
            by=By.CSS_SELECTOR, value="div.old-price"
        )
        old_price = old_price_element.text if old_price_element else None
    except NoSuchElementException:
        old_price = None

    try:
        price = driver.find_element(by=By.CSS_SELECTOR, value="div.regular-price").text
    except NoSuchElementException:
        price = None

    try:
        images = driver.find_elements(by=By.CSS_SELECTOR, value="img.img-fluid")
    except NoSuchElementException:
        images = []

    image_sources = [img.get_attribute("src") for img in images]
    image_sources = list(dict.fromkeys(image_sources))
    image_sources = [base_url + "/" + src for src in image_sources]

    data_list.append(
        {
            "titel": title,
            "rating": rating,
            "descriptie": description,
            "artikel_nummer": article_number,
            "oude_prijs": old_price,
            "prijs": price,
            "fotos": image_sources,
            "page_load_time": page_load_time,
            "status_code": status_code,
        }
    )

    df = pd.DataFrame(data_list)
df.to_csv(
    "Selenium_CSS_Selectors-products_" + port + ".csv", index=False, encoding="utf-8"
)


# Selenium XPath
data_list = []

for link in product_links:
    start_time = time.time()
    driver.get(link)
    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
    custom_js_locator = (By.XPATH, "//script[@src='js/custom.js']")
    wait.until(EC.presence_of_element_located(custom_js_locator))
    end_time = time.time()
    page_load_time = end_time - start_time
    response = driver.execute_async_script(
        "var callback = arguments[arguments.length - 1]; fetch('"
        + link
        + "').then((response) => response.text().then((text) => callback({'status': response.status, 'text': text})))"
    )

    status_code = response["status"]

    try:
        title = driver.find_element(
            by=By.XPATH, value="/html/body/div[1]/div/div/div/div[2]/div/div[2]/h4"
        ).text
    except NoSuchElementException:
        title = None

    try:
        rating_elements = driver.find_elements(
            by=By.XPATH,
            value="/html/body/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div/span[1]/i",
        )
        rating = 5 - len(rating_elements)
    except (NoSuchElementException, TypeError):
        rating = None

    try:
        description = driver.find_element(
            by=By.XPATH, value="/html/body/div[1]/div/div/div/div[2]/div/div[2]/span[1]"
        ).text
    except NoSuchElementException:
        description = None

    try:
        article_number = driver.find_element(
            by=By.XPATH,
            value="/html/body/div[1]/div/div/div/div[2]/div/div[2]/span[2]/b",
        ).text
    except NoSuchElementException:
        article_number = None

    try:
        old_price_element = driver.find_element(
            by=By.XPATH,
            value="/html/body/div[1]/div/div/div/div[2]/div/div[2]/h3/div[2]",
        )
        old_price = old_price_element.text if old_price_element else None
    except NoSuchElementException:
        old_price = None

    try:
        price = driver.find_element(
            by=By.XPATH,
            value="/html/body/div[1]/div/div/div/div[2]/div/div[2]/h3/div[1]",
        ).text
    except NoSuchElementException:
        price = None

    try:
        images = driver.find_elements(
            by=By.XPATH, value='//img[contains(@src, "img/products")]'
        )
    except NoSuchElementException:
        images = []

    image_sources = [img.get_attribute("src") for img in images]
    image_sources = list(dict.fromkeys(image_sources))
    image_sources = [base_url + "/" + src for src in image_sources]

    data_list.append(
        {
            "titel": title,
            "rating": rating,
            "descriptie": description,
            "artikel_nummer": article_number,
            "oude_prijs": old_price,
            "prijs": price,
            "fotos": image_sources,
            "page_load_time": page_load_time,
        }
    )

df = pd.DataFrame(data_list)
df.to_csv("Selenium_XPath-products_" + port + ".csv", index=False, encoding="utf-8")


# Scrapy
product_links = []

import scrapy
from scrapy.http import HtmlResponse


class ProductSpider(scrapy.Spider):
    name = "product_spider"
    start_urls = ["http://localhost:" + port]
    overlopen_urls = []

    def parse(self, response):
        # Vind alle productlinks op de huidige pagina
        product_links = response.css('a[href*="/product_"]::attr(href)').extract()
        self.overlopen_urls.append(response.url)

        for link in product_links:
            yield scrapy.Request(
                url=(base_url + "/" + link), callback=self.parse_product
            )

        # Ga naar de volgende pagina als die er is ==> als de href van de link bevat /?page=
        page_links = response.css('a[href*="/?page="]::attr(href)').extract()
        for link in page_links:
            link = base_url + "/" + link
            if link not in self.overlopen_urls:
                yield scrapy.Request(link, callback=self.parse)

    def parse_product(self, response):
        # Haal productinformatie van de pagina
        title = response.css("h4.product-title::text").extract_first()
        off_classes = response.css("i.off::attr(class)").extract_first()
        rating = 5 - off_classes.count("off")
        description = response.css("span.description::text").extract_first()
        article_number = response.css("span.article-number::text").extract_first()
        old_price = response.css("div.old-price::text").extract_first()
        price = response.css("div.regular-price::text").extract_first()
        image_sources = [
            response.urljoin(img)
            for img in response.css("img.img-fluid::attr(src)").extract()
        ]

        # verwijder image duplicates
        image_sources = list(dict.fromkeys(image_sources))

        yield {
            "titel": title,
            "rating": rating,
            "descriptie": description,
            "artikel_nummer": article_number,
            "oude_prijs": old_price,
            "prijs": price,
            "fotos": image_sources,
            "status_code": response.status,
        }


def main():
    # Voer de crawler uit en sla de gegevens op in een CSV-bestand
    df = pd.DataFrame(
        columns=[
            "titel",
            "rating",
            "descriptie",
            "artikel_nummer",
            "oude_prijs",
            "prijs",
            "fotos",
        ]
    )

    # Voer de spider uit en sla de resultaten op in een DataFrame
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess(
        settings={
            "FEED_FORMAT": "csv",
            "FEED_URI": "scrapy-products_" + port + ".csv",
            "LOG_ENABLED": False,
        }
    )

    process.crawl(ProductSpider)
    process.start()


if __name__ == "__main__":
    main()
    driver.quit()
