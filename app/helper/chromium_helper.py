import os

from app.utils import SystemUtils


class ChromiumHelper(object):
    _playwright = None
    _browser = None
    _context = None
    _page = None
    _headless = False

    def __init__(self, _playwright, headless=False):
        if SystemUtils.is_windows():
            self._headless = False
        elif not os.environ.get("NASTOOL_DISPLAY"):
            self._headless = True
        else:
            self._headless = headless

        try:
            self._playwright = _playwright
            self._browser = self._playwright.chromium.launch(headless=headless)
            desktop_chrome = self._playwright.devices['Desktop Chrome']
            self._context = self._browser.new_context(
                **desktop_chrome,
                timezone_id='Asia/Shanghai',
                locale="zh-CN",
            )
        except Exception as err:
            print(str(err))
            self.close()

    def new_page(self, _url):
        page = self._context.new_page()
        page.set_default_timeout(1000 * 30)
        page.goto(_url)
        page.set_viewport_size({
            "width": 1920,
            "height": 1080
        })
        return page

    def visit(self, _url):
        if not self._page:
            self._page = self.new_page(_url)
        else:
            self._page.goto(_url)
        return self._page

    def close(self):
        if self._context:
            self._context.close()
        if self._browser:
            self._browser.close()