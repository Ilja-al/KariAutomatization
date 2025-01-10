import pytest
from selenium import webdriver

@pytest.fixture
def browser():
    browser = webdriver.Chrome() # открываем Chrome
    browser.maximize_window() # открываем на полную
    browser.implicitly_wait(10) # неявное ожидание 5 секунд
    yield browser