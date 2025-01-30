import pytest
from config.data import Data
from pages.mainpage import MainPage
from pages.regpage import RegPage
from pages.authpage import AuthPage

class BaseTest:

    data: Data

    main_page: MainPage
    reg_page: RegPage
    auth_page: AuthPage

    @pytest.fixture(autouse=True)
    def setup(self, request, browser):
        request.cls.browser = browser
        request.cls.data = Data()
        request.cls.main_page = MainPage(browser)
        request.cls.reg_page = RegPage(browser)
        request.cls.auth_page = AuthPage(browser)