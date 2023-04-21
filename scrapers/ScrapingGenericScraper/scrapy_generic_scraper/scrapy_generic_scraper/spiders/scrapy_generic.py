import json
import os
from dotenv import load_dotenv, find_dotenv
from urllib.parse import urlparse

import scrapy

load_dotenv(find_dotenv())


class MySpider(scrapy.Spider):
    name = 'generic'

    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
        'DUPEFILTER_DEBUG': False,
        'ROBOTSTXT_OBEY': False,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    }

    def apply_selctors(self, selector, response):
        """
        this function will be use selecting which type of selectors we are going to use
        :param selector: tell which type selector css or xpath
        :param response: it will return html format response
        :return: it will return the web page source
        """
        if selector['type'] == 'css':
            selected_data = response.css(selector['value'])
        elif selector['type'] == 'xpath':
            selected_data = response.xpath(selector['value'])
        else:
            raise ValueError(f"Invalid selector type: {selector['type']}")
        return selected_data

    def start_requests(self):
        """
        this function will start the read our json file from the ur folder structure it will return us start url to start scrap
        :return: it will return us start url
        """
        folder_path = os.getenv('ABSOLUTE_PATH_FOR_SCRAPY_START_URLS')
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            with open(file_path) as f:
                start_urls = json.load(f)
                for item in start_urls:
                    yield scrapy.Request(url=item['url'], callback=self.parse,
                                         meta={'selectors': item['selectors'], 'json_items': item})

    def parse(self, response, **kwargs):
        """
        In this function we are going the scrap the data for the single page and also for linked followed pages is available we will scrap
        If is_link_to_follow is true we will go scrapping links from the inside the main pages and is_link_to_follow is false we will scrap the only main page
        There also pagination in the website is present we will scrap all pages present in the website
        :return: it will return specific data that need scrap from the website
        """
        json_item = response.meta.get("json_items")
        domain = json_item['domain_url']
        for selector in response.meta.get('selectors'):
            selected_data = self.apply_selctors(selector, response)
            if selector.get("is_link_to_follow"):
                for url in selected_data.getall():
                    parsed_url = urlparse(url)
                    domain_name = f"{parsed_url.scheme}://{parsed_url.netloc}"
                    final_url = url.replace(domain_name, '')
                    follow_url = domain + final_url
                    yield scrapy.Request(url=follow_url, callback=self.parse_data,
                                         meta={'selectors': json_item.get('data_gathering_selectors'),
                                               'json_items': json_item})
            else:
                for box in selected_data:
                    for data_selector in json_item.get('data_selectors'):
                        selected_data_single_page = self.apply_selctors(data_selector, box)
                        yield {'title': data_selector['title'], 'data': selected_data_single_page.getall()}

        if next_page_selectors := json_item.get('next_page_selectors'):
            if next_page_link := response.xpath(
                next_page_selectors[0].get('value')
            ).get():
                parsed_url = urlparse(next_page_link)
                domain_name = f"{parsed_url.scheme}://{parsed_url.netloc}"
                final_url = next_page_link.replace(domain_name, '')
                follow_url = domain + final_url
                yield scrapy.Request(url=follow_url, callback=self.parse,
                                     meta={'selectors': json_item['selectors'], 'json_items': json_item})

    def parse_data(self, response, **kwargs):
        """
        this function is going scrap the data from the inside links getting from the page. This function will be executed when is_link_to_follow is true
        this function will scrap particular data we needed from the next page
        :return: it will return the particular data need from the website
        """
        data = {'url': response.url, 'selected_data': []}
        for selector in response.meta['selectors']:
            selected_data = self.apply_selctors(selector, response)
            data['selected_data'].append({'title': selector.get('title'), 'data': selected_data.getall()})

        for obj in data['selected_data']:
            obj['data'] = [i.strip() for i in obj['data'] if i.strip()]

        yield data
