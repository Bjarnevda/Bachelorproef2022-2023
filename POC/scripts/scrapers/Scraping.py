import os
import sys
import requests
from bs4 import BeautifulSoup

from BeautifulsoupScrapers import BSselectorScraper, BSxpathScraper
from SeleniumScrapers import SselectorScraper, SxpathScraper
from Scrapy import scrapyScraper

def removeCSV(name):
    if os.path.exists("csvs/" + name + ".csv"):
        os.remove("csvs/" + name + ".csv")
    
def getProducts(base_url, page, headers, product_links=None):
    if product_links is None:
        product_links = []

    url = base_url + "?page=" + str(page)
    response =  requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a")
        product_links_temp = [
            link["href"]
            for link in links
            if link.has_attr("href") and "/product_" in link["href"]
        ]
        product_links.extend(base_url + link for link in product_links_temp)

        next_links = [
            link["href"]
            for link in links
            if link.has_attr("href") and "/?page=" in link["href"]
        ]

        if next_links:
            next_page = int(next_links[-1].split("=")[-1])
            if next_page > page:
                return getProducts(base_url, next_page, headers, product_links)
        return product_links
    else:
        print("Kon de cataloguspagina niet ophalen. Status code:", response.status_code)
        return None

def main():
    port = sys.argv[1]

    base_url = "http://localhost:" + port

    headers = {
    "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    "Accept-Encoding": 'gzip, deflate, br',
    "Accept-Language": 'nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7',
    "Cache-Control": 'max-age=0',
    "Connection": 'keep-alive',
    "Cookie": 'grafana_session=9bfd6bed379744fca238a283406c2cb1; grafana_session_expiry=1692575506',
    "Host": f'localhost:{port}',  
    "Sec-Ch-Ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    "Sec-Ch-Ua-Mobile": '?0',
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": 'document',
    "Sec-Fetch-Mode": 'navigate',
    "Sec-Fetch-Site": 'same-origin',
    "Sec-Fetch-User": '?1',
    "Upgrade-Insecure-Requests": '1',
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    
    product_links = getProducts(base_url, 1, headers)

    # Verwijder de CSV-bestanden als ze bestaan
    removeCSV(port + "_BeautifulSoup_CSS_Selectors")
    removeCSV(port + "_BeautifulSoup_XPath")
    removeCSV(port + "_Selenium_CSS_Selectors")
    removeCSV(port + "_Selenium_XPath")
    removeCSV(port + "_Scrapy")

    BSselectorScraper(base_url, product_links, "csvs/" + port + "_BeautifulSoup_CSS_Selectors.csv",headers)
    BSxpathScraper(base_url, product_links, "csvs/" + port + "_BeautifulSoup_XPath.csv",headers)

    SselectorScraper(base_url, product_links,"csvs/" + port + "_Selenium_CSS_Selectors.csv")
    SxpathScraper(base_url, product_links,"csvs/" + port + "_Selenium_XPath.csv")

    scrapyScraper(base_url, port, "csvs/" + port + "_Scrapy.csv",headers)

if __name__ == "__main__":
    main()
