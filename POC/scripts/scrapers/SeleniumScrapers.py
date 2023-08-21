import pandas as pd
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
def SselectorScraper(base_url,product_links, file_path):

    data_list = []

    for link in product_links:
        start_time = time.time()
        driver.get(link)
        request_time = round((time.time() - start_time) * 1000)
        wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
        image_locator = (By.XPATH, '//*[@id="product-tab-1"]/img')
        wait.until(EC.presence_of_element_located(image_locator))
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
                "request_time": request_time,
            }
        )

    df = pd.DataFrame(data_list)
    df.to_csv(
        file_path, index=False, encoding="utf-8"
    )

# Selenium XPath
def SxpathScraper(base_url,product_links, file_path):

    data_list = []
    
    for link in product_links:
        start_time = time.time()
        driver.get(link)
        wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
        image_locator = (By.XPATH, '//*[@id="product-tab-1"]/img')
        wait.until(EC.presence_of_element_located(image_locator))
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
    df.to_csv(file_path, index=False, encoding="utf-8")
    
    