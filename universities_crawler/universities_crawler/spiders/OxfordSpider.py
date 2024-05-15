from pathlib import Path

import scrapy
from scrapy_playwright.page import PageMethod


class OxfordSpider(scrapy.Spider):
    name = "oxford"
    allowed_domains = ["ox.ac.uk"]
    start_urls = ["https://www.ox.ac.uk/search"]

    def start_requests(self):
        # Submit the search form using Playwright
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    # wait the page to fully load
                    PageMethod("wait_for_load_state", "networkidle"),
                    # accept the cookie policy
                    PageMethod("click", "button#ccc-notify-accept"),
                    # fill in the search
                    PageMethod("fill", "input[name='search']", "digital transformation"),
                    # click submit button
                    PageMethod("click", "button.gsc-search-button"),
                    # wait for an element on the reidrect page
                    PageMethod("wait_for_selector", "div.gsc-expansionArea"),
                    # PageMethod("evaluate", 'document.querySelectorAll(".gsc-cursor-page").forEach(x=>x.click())')
                ],
            }
        )

    def parse(self, response, **kwargs):
        for item in response.css('a.gs-title'):
            url = item.css("::attr(href)").get()
            title = ''.join(item.css("::text").getall()).lower()
            if url:
                yield scrapy.Request(url, callback=self.save_html, cb_kwargs={'title': title})

    def save_html(self, response, title):
        # Define folder paths
        file_name = f"{title}.html"
        folder_path = Path(f"crawled_files/{self.name}")

        # Create folders if they don't exist
        folder_path.mkdir(parents=True, exist_ok=True)

        # Save the HTML content
        with open(folder_path / file_name, "wb") as f:
            f.write(response.body)
        print(f"Saved HTML to: {folder_path / file_name}")
