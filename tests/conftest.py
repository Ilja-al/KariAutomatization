import pytest
import allure
import pymongo
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def browser():
    options = Options()
    options.add_argument('--headless')  # Безголовый режим
    options.add_argument('--disable-gpu')  # Отключение GPU
    options.add_argument('--no-sandbox')  # Полезно для Docker
    options.add_argument('--window-size=1920,1080')  # Размер окна
    options.page_load_strategy = 'none'  # Отключаем ожидание полной загрузки страницы


    browser = webdriver.Chrome(options=options)  # Запуск браузера

    #browser.maximize_window()  # Разворачивание на полный экран
    #browser.implicitly_wait(5)  # Неявное ожидание 5 секунд

    try:
        yield browser
    finally:
        browser.quit()  # Гарантированное закрытие браузера

@pytest.fixture(autouse=True)
def set_allure_labels():
    allure.dynamic.parent_suite('ИМ - Регистрация/авторизация')
    allure.dynamic.suite('ИМ - Регистрация/авторизация')
    allure.dynamic.feature('ИМ - Регистрация/авторизация')


# Фикстура для подключения к MongoDB
@pytest.fixture(scope="module")
def mongo_client():
    # Настройки подключения (замени на свои значения)
    mongo_uri = "mongodb://user:pass@uri:27017"
    database_name = "clients"
    # Подключение к MongoDB
    client = pymongo.MongoClient(mongo_uri)
    db = client[database_name]
    yield db  # Передача объекта базы данных тестам
    # Закрытие подключения после завершения тестов
    client.close()