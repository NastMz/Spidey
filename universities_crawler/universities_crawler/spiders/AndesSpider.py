import os
import uuid

import scrapy
from scrapy_playwright.page import PageMethod

from universities_crawler.items import UniversitiesCrawlerItem

from universities_crawler.utils import clean_content


class AndesSpider(scrapy.Spider):
    name = "andes"

    def start_requests(self):
        # Submit the search form using Playwright
        yield scrapy.Request(
            url="https://uniandes.edu.co/",
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod("click", "div.search-bar"),
                    PageMethod('fill', 'form#buscadorDesktop > input#parametro', 'transformación digital'),
                    PageMethod('press', 'form#buscadorDesktop', 'Enter'),
                    PageMethod('wait_for_selector', 'div.gsc-results-wrapper-nooverlay.gsc-results-wrapper-visible > div.gsc-wrapper')
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
                    ),
                    callback=self.parse_page
                )

    async def parse_page(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        url = response.css("div.download > div.file-section > ds-meta-download > div > a::attr(href)").get()

        if url:
            print("PDF URL: ", url)
            yield scrapy.Request(
                url="https://repositorio.uniandes.edu.co" + url,
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

        page_content = response.css(".content__text, .pane-Descripcin, #postContent")

        if page_content:
            self.logger.info(f"Scraping: {response.url}")

            title = response.css('h1::text').get()

            content = page_content.css("p ::text, li ::text, div.elementor-widget-container ::text").getall()

            cleaned_content = clean_content(content)

            data = UniversitiesCrawlerItem(university="Universidad de los Andes", country="Colombia")

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
        self.logger.error(f"Error: {failure.response.url}")
        page = failure.request.meta["playwright_page"]
        await page.close()
