from playwright.sync_api import Page


def init_page(page: Page) -> None:
    """
    初始化页面，添加反检测脚本
    """
    page.add_init_script(
        """Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"""
    )
