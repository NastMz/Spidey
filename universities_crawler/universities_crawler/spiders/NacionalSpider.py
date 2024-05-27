import os

import scrapy
from scrapy_playwright.page import PageMethod

from universities_crawler.items import UniversitiesCrawlerItem

from universities_crawler.utils import clean_content


class NacionalSpider(scrapy.Spider):
    name = "nacional"

    def start_requests(self):
        # Submit the search form using Playwright
        yield scrapy.Request(
            url="https://unal.edu.co/resultados-de-la-busqueda/?q=trasformaci%C3%B3n+digital",
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod("wait_for_selector", "div.gsc-results-wrapper-nooverlay.gsc-results-wrapper-visible"),
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
            if '.pdf' in url:
                pdf_url = url.split('?')[0]
                yield scrapy.Request(
                    url=pdf_url,
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
                    ),
                    callback=self.parse_page
                )

    async def parse_page(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        url = response.css("div.item-page-field-wrapper.table.word-break > div > a::attr(href)").get()

        if url:
            yield scrapy.Request(
                url="https://repositorio.unal.edu.co" + url.split('?')[0],
                callback=self.save_pdf
            )
        else:
            yield scrapy.Request(
                url=response.url,
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

        page_content = response.css(".article-detail-layout-first")

        if page_content:
            self.logger.info(f"Scraping: {response.url}")

            title = response.css('h1::text').get()

            content = page_content.css("p ::text, li ::text").getall()

            cleaned_content = clean_content(content)

            data = UniversitiesCrawlerItem(university="Universidad Nacional de Colombia", country="Colombia")

            data['title'] = title

            data['content'] = cleaned_content

            yield data

    def save_pdf(self, response):
        path = f"crawled_files/pdf/{self.name}/" + response.url.split('/')[-1]
        dir_name = os.path.dirname(path)

        # Create the directory if it doesn't exist
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        if path.endswith('.pdf'):
            with open(path, 'wb') as file:
                file.write(response.body)

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
