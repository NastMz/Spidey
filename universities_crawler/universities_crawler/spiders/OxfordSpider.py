from pathlib import Path

import scrapy
from scrapy_playwright.page import PageMethod

from universities_crawler.items import UniversitiesCrawlerItem


class OxfordSpider(scrapy.Spider):
    name = "oxford"

    def start_requests(self):
        # Submit the search form using Playwright
        yield scrapy.Request(
            url="https://staff.admin.ox.ac.uk/digital-transformation",
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod("wait_for_selector", "button#ccc-recommended-settings"),
                    PageMethod("click", "button#ccc-recommended-settings"),
                    PageMethod("wait_for_selector", "#main-content"),
                    PageMethod("wait_for_selector", "#listing-wrapper-4186581")
                ],
                errback=self.errback,
            )
        )

    async def parse(self, response, **kwargs):
        page = response.meta["playwright_page"]
        await page.close()

        page_content = response.css("#main-content, .main-content")

        if page_content:
            self.logger.info(f"Crawling: {response.url}")

            title = page_content.css('h1::text').get()

            content = page_content.css('.paragraphs-items ::text').getall()

            cleaned_content = [text.strip().replace(' ', ' ').lower() for text in
                               content]  # Remove leading/trailing whitespace and non-breaking spaces

            if 'digital transformation' in ' '.join(cleaned_content):
                data = UniversitiesCrawlerItem(university="University of Oxford", country="United Kingdom")

                data['title'] = title

                data['content'] = ' '.join(cleaned_content)

                yield data
                urls = page_content.css('.paragraphs-items').css("a::attr(href)").getall()
                for url in urls:
                    if url.lower().startswith("http"):
                        subpage_url = url
                    elif url.startswith("#") or url.startswith("?"):
                        subpage_url = response.url + url
                    else:
                        subpage_url = "https://staff.admin.ox.ac.uk" + url

                    yield scrapy.Request(
                        url=subpage_url,
                        meta=dict(
                            playwright=True,
                            playwright_include_page=True,
                            playwright_page_methods=[
                                PageMethod("wait_for_selector", "#main-content, .main-content")
                            ],
                            errback=self.errback,
                        )
                    )

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
