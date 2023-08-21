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

