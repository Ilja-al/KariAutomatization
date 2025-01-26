from selenium.webdriver.common.by import By
import allure
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class RegPage:

    def __init__(self, browser):
        self.browser = browser

    # Метод для добавления ошибки в Allure-отчёт
    def attach_error(self, title, message):
        allure.attach(message, name=title, attachment_type=allure.attachment_type.TEXT)

    # Метод для ожидания наличия и видимости элемента (работает с CSS и XPath)
    def wait_for_element(self, locator, by=By.XPATH, timeout=10, visible=True):
        try:
            condition = EC.visibility_of_element_located if visible else EC.presence_of_element_located
            return WebDriverWait(self.browser, timeout).until(condition((by, locator)))
        except TimeoutException as e:
            self.attach_error(f"Ошибка ожидания элемента: {locator}", str(e))
            raise

    # Метод для ожидания кликабельности элемента
    def wait_for_clickable_element(self, locator, by=By.XPATH, timeout=10):
        try:
            return WebDriverWait(self.browser, timeout).until(EC.element_to_be_clickable((by, locator)))
        except TimeoutException as e:
            self.attach_error(f"Ошибка ожидания кликабельного элемента: {locator}", str(e))
            raise

    def open_reg_page(self):
        with allure.step('Открыть страницу регистрации'):
            self.browser.get('https://test-not-prod.kari.com/auth/reg/')
            assert 'reg' in self.browser.current_url, 'Не удалось перейти на страницу регистрации'
            button_submit = self.wait_for_clickable_element('//button[text()="Применить"]')
            button_submit.click()

    def reg_input_tel(self):
        """Ввод зарегистрированного номера телефона"""
        with allure.step('Ввести зарегистрированный номер'):
            input_tel_element = self.wait_for_element('//input[@type="tel"]')
            input_tel_element.send_keys('9022779866')
        with allure.step('Нажать "Получить код"'):
            self.wait_for_clickable_element('//button[text()="Получить код"]').click()

    def reg_input_tel_validation(self, phone, error=None):
        """Проверка наличия валидации поля ввода номера телефона"""
        with allure.step('Проверка наличия поля ввода номера телефона'):
            phone_filed = self.wait_for_element('//input[@name="phone"]', By.XPATH)
        with allure.step('Очистка поля ввода номера телефона'):
            phone_filed.clear()
        with allure.step('Заполнить поле (значения указаны в параметризации)'):
            phone_filed.send_keys(phone)
        with allure.step('Нажать "Получить код"'):
            self.wait_for_clickable_element('//button[text()="Получить код"]', By.XPATH).click()
        with allure.step('Проверка наличия ошибки валидации'):
            error_message_element = self.wait_for_element(f"//p[contains(text(), '{error}')]", By.XPATH)
            assert error_message_element.is_displayed(), f"Ошибка: Ожидалось сообщение '{error}', но оно не отображается для {phone}"

    def generate_random_phone(self):
        """Генерирует номер телефона в формате 9XXXXXXXXX."""
        return f"{random.randint(9000000000, 9999999999)}"

    def input_unregistered_tel(self):
        """Ввод незарегистрированного номера телефона в формате 9XXXXXXXXX."""
        with allure.step('Ввести не зарегистрированный номер'):
            random_phone = self.generate_random_phone()
            input_tel_element = self.wait_for_element('//input[@type="tel"]')
            input_tel_element.send_keys(random_phone)
        with allure.step('Нажать "Получить код"'):
            self.wait_for_clickable_element('//button[text()="Получить код"]').click()

    def find_captcha(self):
        with allure.step('Проверка открытия капчи'):
            captcha_element = self.wait_for_element('//h3[text()="А вы точно не робот?"]')
            assert captcha_element.text == "А вы точно не робот?", "Неверный текст в окне капчи."
            return captcha_element