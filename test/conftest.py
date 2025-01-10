import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def browser():
    options = Options()
    options.add_argument('--headless') # опция для запуска в безголовом режиме
    browser = webdriver.Chrome(options=options) # открываем Chrome
    browser.maximize_window() # открываем на полную
    browser.implicitly_wait(10) # неявное ожидание 5 секунд
    yield browser