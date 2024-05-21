from pathlib import Path

import scrapy
from scrapy_playwright.page import PageMethod

from universities_crawler.items import UniversitiesCrawlerItem

from universities_crawler.utils import clean_content


class MunichSpider(scrapy.Spider):
    name = "munich"

    def start_requests(self):
        # Submit the search form using Playwright
        yield scrapy.Request(
            url="https://www.tum.de/en/",
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod("click", "button.btn.btn--search"),
                    PageMethod("fill", "input#search", "digital transformation"),
                    PageMethod("click", "button.btn.btn--search.search__submit"),
                    PageMethod("wait_for_selector", "ul.search__results-items"),
                    PageMethod("click", "div.search__filter > ul > li:nth-child(2)"),
                    PageMethod("click", "div.search__filter > ul > li:nth-child(3)"),
                ],
                errback=self.errback,
            ),
            callback=self.parse_search_page
        )

    async def parse_search_page(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        page_urls = response.css("a.search__results-item::attr(href)").getall()

        for url in page_urls:
            yield scrapy.Request(
                url="https://www.tum.de" + url,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    errback=self.errback,
                )
            )

    async def parse(self, response, **kwargs):
        page = response.meta["playwright_page"]
        await page.close()

        page_content = response.css("#main-content, .news-detail")

        if page_content:
            self.logger.info(f"Scraping: {response.url}")

            title = page_content.css('h1::text').get()

            content = page_content.css('.ce-textmedia').css("p ::text, li ::text").getall()

            cleaned_content = clean_content(content)

            data = UniversitiesCrawlerItem(university="Technical University of Munich", country="Germany")

            data['title'] = title

            data['content'] = cleaned_content

            yield data

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
