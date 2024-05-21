from pathlib import Path

import scrapy
from scrapy_playwright.page import PageMethod

from universities_crawler.items import UniversitiesCrawlerItem

from universities_crawler.utils import clean_content


class ParisSpider(scrapy.Spider):
    name = "paris"

    def start_requests(self):
        # Submit the search form using Playwright
        yield scrapy.Request(
            url="https://psl.eu/en",
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod("click", "button.agree-button.eu-cookie-compliance-default-button"),
                    PageMethod("click", "div.header_block > div > div.search_bouton"),
                    PageMethod("fill", "div#block-custom-theme-search > form > div > div > input#edit-keys", "digital transformation"),
                    PageMethod("click", "div#block-custom-theme-search > form > div > div > span.input-group-btn > button"),
                    PageMethod("wait_for_selector", "div.search-resuts"),
                ],
                errback=self.errback,
            ),
            callback=self.parse_search_page
        )

    async def parse_search_page(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        page_urls = response.css("div.search-resuts > ol > li > h3 > a::attr(href)").getall()

        for url in page_urls:
            yield scrapy.Request(
                url=url,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    errback=self.errback,
                )
            )

    async def parse(self, response, **kwargs):
        page = response.meta["playwright_page"]
        await page.close()

        page_content = response.css(".field--name-field-contenu, .field--name-field-contenue-d-onglet")

        if page_content:
            self.logger.info(f"Scraping: {response.url}")

            title = response.css('section.main_section > div.region.region-content, section.main_section > '
                                 'div.region.region-content > div.f_fiche_formation').css('div.page_with_bar > '
                                                                                          'div.left_part > h1').css(
                'span::text, div::text').get()

            content = page_content.css("p ::text, li ::text").getall()

            cleaned_content = clean_content(content)

            data = UniversitiesCrawlerItem(university="PSL Université Paris", country="France")

            data['title'] = title

            data['content'] = cleaned_content

            yield data

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
