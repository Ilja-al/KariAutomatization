import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.support.ui import WebDriverWait

class BasePage:

    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(browser, 10, poll_frequency=1)

    def make_screenshot(self, screenshot_name):
        allure.attach(
            body=self.browser.get_screenshot_as_png(),
            name=screenshot_name,
            attachment_type=AttachmentType.PNG
        )

