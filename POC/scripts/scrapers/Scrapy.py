import scrapy
from scrapy.crawler import CrawlerProcess
import time

class ProductSpider(scrapy.Spider):
    name = "product_spider"
    overlopen_urls = []

    def __init__(self, base_url, port, headers, *args, **kwargs):
        super(ProductSpider, self).__init__(*args, **kwargs)
        self._port = port
        self._base_url = base_url
        self.start_urls = [f"http://localhost:{self._port}"]
        self._headers = headers

    def parse(self, response):
        # Vind alle productlinks op de huidige pagina
        product_links = response.css('a[href*="/product_"]::attr(href)').extract()
        self.overlopen_urls.append(response.url)

        for link in product_links:
            self.crawl_start_time = time.time() 
            yield scrapy.Request(
                url=(self._base_url + "/" + link), headers=self._headers, callback=self.parse_product
            )

        # Ga naar de volgende pagina als die er is ==> als de href van de link bevat /?page=
        page_links = response.css('a[href*="/?page="]::attr(href)').extract()
        for link in page_links:
            link = self._base_url + "/" + link
            if link not in self.overlopen_urls:
                yield scrapy.Request(link, headers=self._headers, callback=self.parse)

    def parse_product(self, response):
        
        elapsed_time = time.time() - self.crawl_start_time
        request_time = round(elapsed_time * 1000)
        
        # Haal productinformatie van de pagina
        try:
            title = response.css("h4.product-title::text").extract_first()
        except:
            title = None

        try:
            off_classes = response.css("i.off::attr(class)").extract_first()
            rating = 5 - off_classes.count("off")
        except:
            rating = None

        try:
            description = response.css("span.description::text").extract()
        except:
            description = None

        try:
            article_number = response.css("span.article-number").extract()
            article_number = article_number[0]
            article_number = article_number.split("<b>")[1]
            article_number = article_number.split("</b>")[0]
        except:
            article_number = None

        try:
            old_price = response.css("div.old-price::text").extract()
            old_price = old_price[1]
        except:
            old_price = None

        try:
            price = response.css("div.regular-price::text").extract()
            price = price[1]
        except:
            price = None

        try:
            image_sources = [
                response.urljoin(img)
                for img in response.css("img.img-fluid::attr(src)").extract()
            ]
            # verwijder image duplicates
            image_sources = list(dict.fromkeys(image_sources))
        except:
            image_sources = None

        yield {
            "titel": title,
            "rating": rating,
            "descriptie": description,
            "artikel_nummer": article_number,
            "oude_prijs": old_price,
            "prijs": price,
            "fotos": image_sources,
            "status_code": response.status,
            "request_time": request_time,
        }


def scrapyScraper(base_url,port, file_path,headers):
    process = CrawlerProcess(
        settings={
            "FEED_FORMAT": "csv",
            "FEED_URI": file_path,
            "LOG_ENABLED": False,
        }
    )

    process.crawl(ProductSpider, base_url=base_url, port=port, headers=headers)
    process.start()

