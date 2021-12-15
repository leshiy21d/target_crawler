import scrapy
from targer_crawler.items import ProductsItem
from scrapy_playwright.page import PageCoroutine
from src import selectors


class TargetCrawlerSpider(scrapy.Spider):
    name = 'target_crawler'
    allowed_domains = ['target.com']
    start_urls = ['http://target.com/']

    URL = 'https://www.target.com/p/consumer-cellular-moto-g-32gb-play/-/A-82040157'

    def start_requests(self):
        yield scrapy.Request(url=TargetCrawlerSpider.URL,
                             meta=dict(
                                 playwright=True,
                                 playwright_include_page=True,
                                 playwright_page_coroutine=[
                                     PageCoroutine('wait_for_selector', '.h-flex-align-baseline')])
                             )

    async def parse(self, response):

        list_of_images = [image for image in response.css(selectors.IMAGES_SELECTOR).getall() if "https://target" in image]

        product_item = ProductsItem()
        product_item['title'] = response.css(selectors.TITLE_SELECTOR).extract_first(),
        product_item['price'] = response.css(selectors.PRICE_SELECTOR).extract_first(),
        product_item['images'] = list_of_images,
        product_item['description'] = response.css(selectors.DESCRIPTION_SELECTOR).extract_first(),
        product_item['product_highlights'] = response.css(selectors.HIGHLIGHTS_SELECTOR).getall()

        # TODO find the way to effectively interact with Q&A tab

        yield product_item
