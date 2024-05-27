import os
import uuid

import scrapy
from scrapy_playwright.page import PageMethod

from universities_crawler.items import UniversitiesCrawlerItem

from universities_crawler.utils import clean_content


class CambridgeSpider(scrapy.Spider):
    name = "cambridge"

    def start_requests(self):
        # Submit the search form using Playwright
        yield scrapy.Request(
            url="https://search.cam.ac.uk/web",
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod("fill", "input#query", "digital transformation"),
                    PageMethod("click", "button.btn.btn-primary[type='submit']"),
                    PageMethod("wait_for_selector", "div#search-results-content"),
                    PageMethod('click', 'div.card.search-facet > div.card-body > ul.list-unstyled > li:nth-child(2) > a'),
                    PageMethod("wait_for_selector", "div#search-results-content"),
                ],
                errback=self.errback,
                playwright_context_kwargs=dict(
                    ignore_https_errors=True,
                )
            ),
            callback=self.parse_search_page
        )

    async def parse_search_page(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        page_urls = response.css("div.card-header").css("a::attr(title)").getall()

        for url in page_urls:
            yield scrapy.Request(
                url=url
            )

    def parse(self, response, **kwargs):
        pathnames = response.url.split('/')

        if '.pdf' in pathnames[-1]:
            file_name = pathnames[-1]
        else:
            # generate random name
            file_name = "pdf_" + str(uuid.uuid4()) + ".pdf"

        self.logger.info(f"Saving PDF: {file_name}")

        path = f"crawled_files/pdf/{self.name}/" + file_name
        dir_name = os.path.dirname(path)

        # Create the directory if it doesn't exist
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        with open(path, 'wb') as file:
            file.write(response.body)

    async def errback(self, failure):
        self.logger.error(f"Error: {failure.response.url}")
        page = failure.request.meta["playwright_page"]
        await page.close()