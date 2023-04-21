import scrapy


class SbsNhsScraperSpider(scrapy.Spider):
    name = "sbs_nhs_scraper"
    allowed_domains = ["sbs.nhs.uk"]

    def start_requests(self):
        url = 'https://www.sbs.nhs.uk/framework-agreement-search'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        framework_page_link = response.css('a.card__link.card__link--heading::attr(href)').getall()
        for framework in framework_page_link:
            yield response.follow(url=f'https://www.sbs.nhs.uk/{framework}', callback=self.framework_parse)

    def framework_parse(self, response):
        framework_name = response.css('h1.a-heading__title::text').get()
        dates = response.css(
            'p:not(strong):contains("start?")::text,p:not(strong):contains("What is the framework agreement '
            'duration")::text,p:not(strong):contains("Term of the framework agreement")::text').get()
        lots = response.xpath('//text()[contains(., "• Lot") and not(. = following::text()[contains(., "• Lot")])]').getall()
        if not lots:
            lots = response.xpath("//table[@class='d1general']/tbody/tr/td[2]/p/text()").getall()

        suppliers = response.xpath(
            "//table[@class='d1general']/tbody/tr/td[3]/p/text() | //*[@id='maincontent']/div[1]/div[3]/div/div["
            "3]/table/tbody/tr/td/p/text()").getall()
        print(
            f'framework_name-------------{framework_name}\nDate-----:{dates}\nlots:---------{lots}\nsuppliers---------{suppliers}')
