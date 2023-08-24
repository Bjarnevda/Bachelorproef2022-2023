import datetime
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


def getProducts(base_url, page, headers, visited_pages=None, product_links=None):
    if product_links is None:
        product_links = []
    if visited_pages is None:
        visited_pages = set()

    if page in visited_pages:
        return product_links

    visited_pages.add(page)

    print("Scraping catalogus page", page)

    url = base_url + "?page=" + str(page)
    response = requests.get(url, headers=headers)

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

        for next_link in next_links:
            next_page = int(next_link.split("=")[-1])
            if next_page >= 2:
                continue
            product_links = getProducts(
                base_url, next_page, headers, visited_pages, product_links
            )
        return product_links
    else:
        print("Kon de cataloguspagina niet ophalen. Status code:", response.status_code)
        return None


def writeTimeScraped(base_url, port, scraperName, done):
    if done:
        content_to_append = (
            base_url
            + ","
            + port
            + "WITH"
            + scraperName
            + "DONE AT:"
            + str(datetime.datetime.now())
        )
    else:
        content_to_append = (
            base_url
            + ","
            + port
            + "WITH"
            + scraperName
            + " STARTED AT:"
            + str(datetime.datetime.now())
        )

    with open("ScrapingsTijden.txt", "a") as file:
        file.write(content_to_append + "\n")


def main():
    port = sys.argv[1]

    base_url = "http://localhost:" + port

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "grafana_session=9bfd6bed379744fca238a283406c2cb1; grafana_session_expiry=1692575506",
        "Host": f"localhost:{port}",
        "Sec-Ch-Ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    }

    print("Getting product links")
    product_links = getProducts(base_url, 1, headers)

    print("removing CSV's")
    # Verwijder de CSV-bestanden als ze bestaan
    removeCSV(port + "_BeautifulSoup_CSS_Selectors")
    removeCSV(port + "_BeautifulSoup_XPath")
    removeCSV(port + "_Selenium_CSS_Selectors")
    removeCSV(port + "_Selenium_XPath")
    removeCSV(port + "_Scrapy")

    """
    writeTimeScraped(base_url, port, "BeautifulSoup_CSS_Selectors", False)
    print("Scraping with BeautifulSoup CSS Selectors")
    BSselectorScraper(
        base_url,
        product_links,
        "csvs/" + port + "_BeautifulSoup_CSS_Selectors.csv",
        headers,
    )
    writeTimeScraped(base_url, port, "BeautifulSoup_CSS_Selectors", True)

    writeTimeScraped(base_url, port, "BeautifulSoup_XPath", False)
    print("Scraping with BeautifulSoup XPath")
    BSxpathScraper(
        base_url, product_links, "csvs/" + port + "_BeautifulSoup_XPath.csv", headers
    )
    writeTimeScraped(base_url, port, "BeautifulSoup_XPath", True)

    writeTimeScraped(base_url, port, "Selenium_CSS_Selectors", False)
    print("Scraping with Selenium CSS Selectors")
    SselectorScraper(
        base_url, product_links, "csvs/" + port + "_Selenium_CSS_Selectors.csv"
    )
    writeTimeScraped(base_url, port, "Selenium_CSS_Selectors", True)

    writeTimeScraped(base_url, port, "Selenium_XPath", False)
    print("Scraping with Selenium XPath")
    SxpathScraper(base_url, product_links, "csvs/" + port + "_Selenium_XPath.csv")
    writeTimeScraped(base_url, port, "Selenium_XPath", True)
"""
    writeTimeScraped(base_url, port, "Scrapy", False)
    print("Scraping with Scrapy")
    scrapyScraper(base_url, port, "csvs/" + port + "_Scrapy.csv", headers)
    writeTimeScraped(base_url, port, "Scrapy", True)


if __name__ == "__main__":
    main()
