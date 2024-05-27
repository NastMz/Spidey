import os

import scrapy
from scrapy_playwright.page import PageMethod

from universities_crawler.items import UniversitiesCrawlerItem

from universities_crawler.utils import clean_content


class CampinasSpider(scrapy.Spider):
    name = "campinas"

    def start_requests(self):
        # Submit the search form using Playwright
        yield scrapy.Request(
            url="https://www.unicamp.br/en/",
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod('click', 'button.gsc-search-button.gsc-search-button-v2'),
                    PageMethod('fill', 'input#gsc-i-id1', 'digital transformation'),
                    PageMethod('click', 'button.gsc-search-button.gsc-search-button-v2'),
                    PageMethod("wait_for_selector", "div.gsc-results-wrapper-overlay.gsc-results-wrapper-visible"),
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
            if '.pdf' in url or 'download' in url:
                yield scrapy.Request(
                    url=url,
                    callback=self.save_pdf
                )
            else:
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

        page_content = response.css(".content")

        if page_content:
            self.logger.info(f"Scraping: {response.url}")

            title = response.css('h1::text').get()

            content = page_content.css("p ::text, li ::text").getall()

            cleaned_content = clean_content(content)

            data = UniversitiesCrawlerItem(university="Universidad de Campinas", country="Brasil")

            data['title'] = title

            data['content'] = cleaned_content

            yield data

    def save_pdf(self, response):
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
        page = failure.request.meta["playwright_page"]
        await page.close()
