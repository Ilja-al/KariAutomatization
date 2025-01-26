from selenium.webdriver.common.by import By
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class MainPage:

    def __init__(self, browser):
        self.browser = browser

    # Метод для ожидания наличия элемента (работает с CSS и XPath)
    def wait_for_element(self, locator, by=By.XPATH, timeout=10):
        try:
            return WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located((by, locator))
            )
        except TimeoutException as e:
            allure.attach(str(e), name=f"Ошибка ожидания элемента: {locator}",
                          attachment_type=allure.attachment_type.TEXT)
            raise

    # Метод для ожидания кликабельности элемента
    def wait_for_clickable_element(self, locator, by=By.XPATH, timeout=10):
        try:
            return WebDriverWait(self.browser, timeout).until(
                EC.element_to_be_clickable((by, locator))
            )
        except TimeoutException as e:
            allure.attach(str(e), name=f"Ошибка ожидания кликабельного элемента: {locator}",
                          attachment_type=allure.attachment_type.TEXT)
            raise

    # Метод для проверки видимости элемента
    def check_element_displayed(self, locator, by=By.XPATH):
        element = self.wait_for_element(locator, by)
        assert element.is_displayed(), f"Элемент {locator} не отображается"
        return element

    def open_main_page(self):
        with allure.step('Открыть сайт'):
            self.browser.get('https://test-not-prod.kari.com/')
            assert 'https://test-not-prod.kari.com/' in self.browser.current_url, 'Не удалось открыть сайт'
            button_submit = self.wait_for_clickable_element('//button[text()="Применить"]')
            button_submit.click()

    def click_login_icon(self): # Иконка входа
        with allure.step('Нажать иконку входа'):
            try:
                login_icon = self.wait_for_clickable_element('//button[@class="css-1svjifm e2cllgv3"]')
                login_icon.click()
            except TimeoutException:
                print("Ошибка: Иконка входа не стала кликабельной за 10 секунд.")

    def click_enter_registration(self): # войти или зарегистрироваться
        with allure.step('Нажать "Войти или зарегистрироваться"'):
            try:
                enter_registration = self.wait_for_clickable_element('//a[@class="css-oc613h e1bfq77c24"]')
                enter_registration.click()
            except TimeoutException:
                print("Ошибка: Ссылка 'Войти или зарегистрироваться' не стала кликабельной за 10 секунд.")