# coding: utf-8
from urllib.parse import quote

from playwright.sync_api import sync_playwright

from app.helper.chromium_helper import ChromiumHelper
from config import Config


class Boxmp4Spider(object):
    torrents_info_array = []
    result_num = 100

    def __init__(self):
        self.init_config()

    def init_config(self):
        self.torrents_info_array = []
        self.result_num = Config().get_config('pt').get('site_search_result_num') or 100

    def search(self, keyword, indexer):

        with sync_playwright() as playwright:
            try:
                chromium = ChromiumHelper(playwright)
                # 请求路径
                torrentspath = indexer.search.get('paths', [{}])[0].get('path', '') or ''
                search_url = indexer.domain + torrentspath.replace("{keyword}", quote(keyword))
                page = chromium.visit(search_url)

                item_eles = page.locator('//*[@id="list_all"]/ul/li')
                count = item_eles.count()
                items = []
                for i in range(count):
                    item_ele = item_eles.nth(i)
                    page_url = item_ele.locator("//a").nth(0).get_attribute("href")
                    title = item_ele.locator("//div/h2").inner_text()
                    if item_ele.locator("//div/*[contains(string(), '别名∶')]").count() != 0:
                        sub_title = item_ele.locator("//div/*[contains(string(), '别名∶')]").inner_text().replace(
                            '别名∶', '')
                    description = item_ele.locator('//div/*[contains(@class, "info")]').inner_text()

                    items.append({
                        "title": title,
                        "sub_title": sub_title,
                        "description": description,
                        "page_url": page_url,
                    })

                for item in items:
                    page.goto(indexer.domain + item["page_url"])
                    download_divs = page.locator('// div[contains(@id, "download")]')
                    download_div_count = download_divs.count()
                    for j in range(download_div_count):
                        rows = page.locator(f'// *[ @ id = "download{j + 1}"] / ul / li')
                        count = rows.count()
                        for k in range(count):
                            row = rows.nth(k).locator("//div[1] / a")
                            name = row.text_content()
                            download_link = row.get_attribute("href")
                            if download_link.lower().startswith("magnet:") \
                                    or download_link.lower().startswith("http:") \
                                    or download_link.lower().startswith("https:") \
                                    or download_link.lower().startswith("bc://bt/"):
                                description = f"{item['sub_title']} {item['description']}" if item['sub_title'] else \
                                    item['description']
                                self.torrents_info_array.append({
                                    "indexer": indexer,
                                    "title": name,
                                    "description": description,
                                    "page_url": item["page_url"],
                                    "enclosure": download_link
                                })
                                if len(self.torrents_info_array) >= int(self.result_num):
                                    break
            finally:
                if chromium:
                    chromium.close()

        return self.torrents_info_array
