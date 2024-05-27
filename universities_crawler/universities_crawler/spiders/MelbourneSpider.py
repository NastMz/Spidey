from pathlib import Path

import scrapy
from scrapy_playwright.page import PageMethod

from universities_crawler.items import UniversitiesCrawlerItem

from universities_crawler.utils import clean_content


class MelbourneSpider(scrapy.Spider):
    name = "melbourne"

    def start_requests(self):
        # Submit the search form using Playwright
        yield scrapy.Request(
            url="https://www.unimelb.edu.au/",
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod("click", "li.mega-menu-alt__search"),
                    PageMethod("wait_for_selector", "div.page-header-search.active"),
                    PageMethod("fill", "div.page-header-search.active > div > div > form > div > input.inline-search__input", "digital transformation"),
                    PageMethod("click", "div.page-header-search.active > div > div > form > div > button.inline-search__submit"),
                    PageMethod("wait_for_selector", "div#toggle-search-vis > ol.list-unstyled"),
                    PageMethod("click", "div#search-tabs > ul > li:nth-child(4)"),
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

        page_urls = response.css("div.search-result__card > div > div > h4 > a::attr(href)").getall()

        for url in page_urls:
            yield scrapy.Request(
                url="https://search.unimelb.edu.au" + url,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    errback=self.errback,
                    playwright_context_kwargs=dict(
                        ignore_https_errors=True,
                    )
                )
            )

    async def parse(self, response, **kwargs):
        page = response.meta["playwright_page"]
        await page.close()

        page_content = response.css(".pr-article-layout__body.pr-content, #main-content")

        if page_content:
            self.logger.info(f"Scraping: {response.url}")

            title = response.css('h1::text').get()

            content = page_content.css("p ::text, li ::text").getall()

            cleaned_content = clean_content(content)

            data = UniversitiesCrawlerItem(university="The University of Melbourne", country="Australia")

            data['title'] = title

            data['content'] = cleaned_content

            yield data

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
