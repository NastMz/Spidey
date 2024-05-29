from pathlib import Path

import scrapy
from scrapy_playwright.page import PageMethod

from universities_crawler.items import UniversitiesCrawlerItem


class TorontoSpider(scrapy.Spider):
    name = "toronto"

    def start_requests(self):
        # Submit the search form using Playwright
        yield scrapy.Request(
            url="https://www.ugr.es/en/search/node?keys=digital+transformation",
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod("wait_for_selector", "div#block-googlecse"),
                    PageMethod("wait_for_selector","div#google-cse-results>div.gsc-expansionArea")
                ],
                errback=self.errback,
            )
        )

    async def parse(self, response, **kwargs):
        page = response.meta["playwright_page"]
        await page.close()

        #aqui empiezo yo
        page_content = response.css("div#google-cse-results>div.gsc-expansionArea>div.gs-title>a::attr(href)").getall()

        import pdb
        pdb.set_trace()

        if page_content:
            self.logger.info(f"Crawling: {response.url}")

            title = page_content.css('h1::text').get()

            content = page_content.css('div.content-field>p ::text').getall()

            cleaned_content = [text.strip().replace(' ', ' ').lower() for text in
                               content]  # Remove leading/trailing whitespace and non-breaking spaces

            if 'digital transformation' in ' '.join(cleaned_content):
                data = UniversitiesCrawlerItem(university="University of Toronto", country="America")

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



    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
