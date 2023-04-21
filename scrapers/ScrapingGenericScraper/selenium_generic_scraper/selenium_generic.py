import json
import logging
import os

from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from dotenv import load_dotenv, find_dotenv
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(level=logging.INFO)
default_value = 'NA'
load_dotenv(find_dotenv())

folder_path = os.getenv('ABSOLUTE_PATH_FOR_SELENIUM_START_URLS')
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    with open(file_path) as f:
        start_urls = json.load(f)


def scrape_url(url, selectors, selected_data_web):
    """
    this function will scrap the data for the content will present on main page or data are find in sub-page
    this function will run for sub link data scrap when is_link_to_follow is true and in case is_link_to_follow is false will scrap all the data main page
    this page will also scrap data if pagintion present in  the website.
    :param url: scrap page url will give
    :param selectors: either is xpath or css selector selecting data web page
    :param selected_data_web: it is the list we will append our data that we have scraped
    :return: it will return the data that we want from the website
    """
    driver.get(url)
    for selector in selectors:
        elements = apply_selectors(selector)
        for element in elements:
            if selector.get('is_link_to_follow'):
                if sub_url := get_element_attribute(element, selector.get('attribute')):
                    sub_data = scrap_data(sub_url, item.get('data_gathering_selectors'))
                    result_data = {'url': sub_url, 'selected_data': sub_data}
                    selected_data_web.append(result_data)
            else:
                result_data = {'url': driver.current_url, 'selected_data': []}
                data_selectors = item.get('data_selectors')
                for data_selector in data_selectors:
                    if selector.get('type') == 'xpath':
                        result_data['selected_data'].append({
                            'title': selector.get('title'),
                            'data': driver.find_element(By.XPATH, data_selector.get('value')).get_attribute(
                                data_selector.get('attribute'))
                        })
                    elif selector.get('type') == 'css':
                        result_data['selected_data'].append({
                            'title': selector.get('title'),
                            'data': driver.find_element(By.CSS_SELECTOR, data_selector.get('value')).get_attribute(
                                data_selector.get('attribute'))
                        })
                selected_data_web.append(result_data)
    if next_page_selectors := item.get('next_page_selectors'):
        if next_page := custom_find_element_by_xpath(
                driver, next_page_selectors[0].get('value')
        ):
            next_page.click()
            scrape_url(driver.current_url, selectors, selected_data_web)


def scrap_data(url, selectors):
    """
    this function will scrap data from the links present in the page. means scrap the data for inner links present in the main page
    :param url: it will take url of data-page for scrap
    :param selectors: we have justify selecting data either xpath or css
    :return: it will return the data that we need scrap from the data-page
    """
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)
    temp = []

    for selector in selectors:
        elements = apply_selectors(selector)
        if result_data := [
            {
                'title': selector['title'],
                'data': get_element_attribute(
                    element, selector.get('attribute')
                ),
            }
            for element in elements

        ]:
            temp.append(result_data[0])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return temp


def apply_selectors(selector):
    """
    this function going select which type path we have given either css or Xpath.
    it will wait through error path type is not css or xpath also stay on that for 10 sec if path not responding after that error will arise
    :param selector: it will select type either xpath or css
    :return: it will return data for the particular select path
    """
    if selector.get('type') == 'css':
        try:
            elements = WebDriverWait(driver, timeout=10).until(
                lambda d: d.find_elements(By.CSS_SELECTOR, selector.get('value')))
        except TimeoutException:
            logging.info(f"Could not find element with CSS selector: {selector.get('value')}")
            elements = [default_value]
    elif selector['type'] == 'xpath':
        try:
            elements = WebDriverWait(driver, timeout=10).until(
                lambda d: d.find_elements(By.XPATH, selector.get('value')))
        except TimeoutException:
            logging.info(f"Could not find element with CSS selector: {selector.get('value')}")
            elements = [default_value]
    else:
        raise ValueError(f"Invalid selector type: {selector.get('type')}")

    return elements


def get_element_attribute(element, attribute):
    """
    this function will get our attribute given in the json file is either innerText or innerHTML etc...
    :param attribute: it will take parma like its innerText or innerHTML etc...
    :return: it will return proper content by removing html tags from the content
    """
    if isinstance(element, str):
        return element
    return element.get_attribute(attribute)


def custom_find_element_by_xpath(driver, element_xpath):
    """
    this function is overwritten the method the find elements
    :param element_xpath: it will take xpath given
    :return: it will return us data if xpath is getting otherwise it will return the none to us
    """
    try:
        element = driver.find_element(By.XPATH, element_xpath)
    except NoSuchElementException:
        element = None
    return element


if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.headless = False
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    selected_data = []

    for item in start_urls:
        get_selectors = item.get('selectors')
        start_url = item.get('url')
        scrape_url(start_url, get_selectors, selected_data)
    with open("result_link_follow.json", "w") as json_file:
        json.dump(selected_data, json_file)