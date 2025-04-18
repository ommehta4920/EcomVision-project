# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

# Selenium Imports
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class SeleniumMiddleware:
    def __init__(self):
        """Initialize Selenium WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run without UI
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def process_request(self, request, spider):
        """Handle requests using Selenium if required"""
        if request.meta.get("use_selenium", False):
            self.driver.get(request.url)
            time.sleep(3)  # Adjust based on the website loading time

            # Return the Selenium-processed response
            return HtmlResponse(url=request.url, body=self.driver.page_source, encoding="utf-8", request=request)

    def __del__(self):
        """Close the WebDriver when middleware is destroyed"""
        self.driver.quit()


class EcomScraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class EcomScraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

import random
import logging
from urllib.parse import urlparse

class proxyMiddleware:
    def __init__(self):
        """Load proxies from file and validate them."""
        self.proxy_list = self.load_proxies("Proxy List.txt")

    def load_proxies(self, file_path):
        """Read proxies and filter invalid ones."""
        valid_proxies = []
        with open(file_path, "r") as file:
            for line in file:
                proxy = line.strip()
                if self.is_valid_proxy(proxy):
                    valid_proxies.append(proxy)
                else:
                    logging.warning(f"Invalid proxy format: {proxy}")
        return valid_proxies

    def is_valid_proxy(self, proxy):
        """Check if proxy URL is properly formatted."""
        parsed = urlparse(proxy)
        return bool(parsed.scheme and parsed.hostname and parsed.port)

    def process_request(self, request, spider):
        """Assign a random proxy to each request."""
        if self.proxy_list:
            proxy = random.choice(self.proxy_list)
            request.meta["proxy"] = proxy
            spider.logger.info(f"Using Proxy: {proxy}")