import scrapy
from scrapy_playwright.page import PageMethod

from universities_crawler.items import UniversitiesCrawlerItem

from universities_crawler.utils import clean_content


class StanfordSpider(scrapy.Spider):
    name = "stanford"

    def start_requests(self):
        # Submit the search form using Playwright
        yield scrapy.Request(
            url="https://www.stanford.edu/search",
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod("fill", "input#search-field", "digital transformation"),
                    PageMethod("click", "button#search-btn"),
                    PageMethod("wait_for_selector", "div.gsc-expansionArea")
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

        page_urls = response.css("a.gs-title::attr(href)").getall()

        for url in page_urls:
            yield scrapy.Request(
                url=url,
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

        page_content = response.css("#main-content, .block-gsb-content, #block-stanfordonline-content")

        if page_content:
            self.logger.info(f"Scraping: {response.url}")

            title = page_content.css('h1::text').get()

            content = page_content.css("#overview, .node__programs-group-left, #block-stanfordonline-content").css(
                'p::text, li::text').getall()

            cleaned_content = clean_content(content)

            data = UniversitiesCrawlerItem(university="Stanford University", country="United States")

            data['title'] = title

            data['content'] = cleaned_content

            yield data

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
