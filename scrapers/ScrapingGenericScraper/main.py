from scrapy.crawler import CrawlerProcess
from selenium_generic_scraper.selenium_generic import selenium_main
from scrapy_generic_scraper.scrapy_generic_scraper.spiders.scrapy_generic import MySpider


def main():
    process = CrawlerProcess()
    process.crawl(MySpider)
    process.start()
    selenium_main()


if __name__ == "__main__":
    main()

