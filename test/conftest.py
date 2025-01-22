import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def browser():
    options = Options()
    options.add_argument('--headless')  # Безголовый режим
    options.add_argument('--disable-gpu')  # Отключение GPU
    options.add_argument('--no-sandbox')  # Полезно для Docker
    options.add_argument('--window-size=1920,1080')  # Размер окна

    browser = webdriver.Chrome(options=options)  # Запуск браузера

    #browser.maximize_window()  # Разворачивание на полный экран
    #browser.implicitly_wait(5)  # Неявное ожидание 5 секунд

    try:
        yield browser
    finally:
        browser.quit()  # Гарантированное закрытие браузера