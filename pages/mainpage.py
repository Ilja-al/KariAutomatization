from selenium.webdriver.common.by import By
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base.base_page import BasePage
from config.links import Links


class MainPage(BasePage):

    # Метод для ожидания наличия элемента (работает с CSS и XPath)
    def wait_for_element(self, locator, by=By.XPATH, timeout=30):
            return WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located((by, locator))
            )

    # Метод для ожидания кликабельности элемента
    def wait_for_clickable_element(self, locator, by=By.XPATH, timeout=30):
            return WebDriverWait(self.browser, timeout).until(
                EC.element_to_be_clickable((by, locator))
            )

    # Метод для проверки видимости элемента
    def check_element_displayed(self, locator, by=By.XPATH):
        element = self.wait_for_element(locator, by)
        assert element.is_displayed(), f"Элемент {locator} не отображается"
        return element

    def open_main_page(self):
        with allure.step('Открыть сайт'):
            page_url = Links.HOST
            print(f"Попытка открыть сайт: {page_url}")  # Выводим, какой URL пытаемся открыть
            self.browser.get(page_url)
            # Печатаем текущий URL после загрузки страницы
            print(f"Текущий URL: {self.browser.current_url}")
            # Ожидаем, что в URL будет содержаться `page_url`
            WebDriverWait(self.browser, 30).until(
                EC.url_contains(page_url)
            )
            # Печатаем, если сайт все-таки не открылся как нужно
            if page_url not in self.browser.current_url:
                print(f"Ошибка: Ожидался URL: {page_url}, но фактический URL: {self.browser.current_url}")
            assert page_url in self.browser.current_url, 'Не удалось открыть сайт'
            print("Ожидание загрузки кнопки")
            button_submit = self.wait_for_clickable_element('//button[text()="Применить"]')
            print("Элемент найден, кликаем по кнопке...")
            button_submit.click()

    def click_login_icon(self): # Иконка входа
        with allure.step('Нажать иконку входа'):
                login_icon = self.wait_for_clickable_element('//button[@class="css-1svjifm e2cllgv3"]')
                login_icon.click()

    def click_enter_registration(self): # войти или зарегистрироваться
        with allure.step('Нажать "Войти или зарегистрироваться"'):
                enter_registration = self.wait_for_clickable_element('//a[@class="css-oc613h e1bfq77c24"]')
                enter_registration.click()
