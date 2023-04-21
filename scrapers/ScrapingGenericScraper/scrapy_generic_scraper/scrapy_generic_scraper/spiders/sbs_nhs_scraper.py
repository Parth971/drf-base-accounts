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
        next_page_link = response.xpath("//a[@class='paging__link paging__link--next']/@href").get()
        if next_page_link:
            yield scrapy.Request(url=next_page_link, callback=self.parse)

    def framework_parse(self, response):
        framework_name = response.css('h1.a-heading__title::text').get()
        dates = response.xpath("//*[contains(text(), ' ') and contains(text(), '20') and contains(text(), 'January') "
                               "or contains(text(), 'February') or contains(text(), 'March') or contains(text(), "
                               "'April') or contains(text(), 'May') or contains(text(), 'June') or contains(text(), "
                               "'July') or contains(text(), 'August') or contains(text(), 'September') or contains("
                               "text(), 'October') or contains(text(), 'November') or contains(text(), "
                               "'December')]/text()").get()
        lots = response.xpath('//*[contains(translate(text(),"LOT","lot"), "lot ") and contains(translate('
                              'substring-after(text(),"lot "), "ABCDEFGHIJKLMNOPQRSTUVWXYZ",'
                              '"abcdefghijklmnopqrstuvwxyz"), translate(substring-after(text(),"lot "), "0123456789", '
                              '""))]//text()[not(normalize-space()=preceding::*/text())]').getall()
        lots = set(lots)
        services = response.xpath('//p[strong[contains(text(),"benefits")]]//text()').getall()
        document = response.css('a.media-link--pdf::attr(href)').get()
        h3 = response.xpath(
            "//h3[contains(text(), 'Which suppliers are on the framework agreement?') or contains(text(), 'Supplier "
            "Details')]")
        if h3:
            # Get the first sibling tag of the h3 tag
            sibling = h3.xpath("following-sibling::*[1]")
            # Get all the a tags in the sibling tag
            a_tags = sibling.xpath(".//a")
            # Extract the href and text values of each a tag
            results = [(a.xpath("text()").get(), a.xpath("@href").get()) for a in a_tags]
            # Use the zip function to create a list of tuples where the text is the key and the href is the value
            suppliers = dict(zip([result[0] for result in results], [result[1] for result in results]))
            yield {'Framework Name': framework_name, 'dates': dates, 'lots': lots, 'suppliers': suppliers,
                   'services': services, 'document': document}
        else:
            yield {'Framework Name': framework_name, 'dates': dates, 'lots': lots, 'services': services,
               'document': document}
