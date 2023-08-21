from bs4 import BeautifulSoup
from lxml import html
import requests
import pandas as pd

# CSS selectors BS4

def BSselectorScraper(base_url, product_links,file_path,headers):
    data_list = []
    for link in product_links:
        response = requests.get(link,headers=headers)

        request_time = round(response.elapsed.total_seconds() * 1000)
    
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
                "request_time": request_time,
            }
        )

    df = pd.DataFrame(data_list)
    df.to_csv(file_path, index=False, encoding="utf-8")

# XPath BS4

def BSxpathScraper(base_url, product_links,file_path,headers):
    data_list = []
    for link in product_links:
        response = requests.get(link,headers=headers)
        request_time = round(response.elapsed.total_seconds() * 1000)
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
                "request_time": request_time,
            }
        )

    df = pd.DataFrame(data_list)
    df.to_csv(file_path,index=False, encoding="utf-8")
