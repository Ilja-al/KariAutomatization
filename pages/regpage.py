from selenium.webdriver.common.by import By
import allure
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
import time

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
        try:
            with allure.step('Открыть форму регистрации'):
                start_time = time.time()
                self.browser.get('https://test-not-prod.kari.com/auth/reg/')
                load_time = time.time() - start_time
                allure.attach(f"Время загрузки страницы: {load_time:.2f} сек", name="Загрузка страницы",
                              attachment_type=allure.attachment_type.TEXT)
                assert 'reg' in self.browser.current_url, 'Не удалось перейти на страницу регистрации'
                try:
                    button_submit = self.wait_for_clickable_element('//button[text()="Применить"]')
                    allure.attach("Кнопка найдена", name="Состояние кнопки",
                                attachment_type=allure.attachment_type.TEXT)
                    button_submit.click()
                except TimeoutException:
                    allure.attach("Кнопка 'Применить' не найдена. Шаг пропущен.", name="Состояние кнопки",
                                  attachment_type=allure.attachment_type.TEXT)
        except WebDriverException as e:
            self.attach_error("Ошибка при открытии страницы", str(e))
            raise

    def reg_check(self):
        header_element = self.wait_for_element('//h1')
        assert "Регистрация" in header_element.text, f"Ожидался текст 'Регистрация', но найден: {header_element.text}"
        return header_element

    def reg_input_tel(self):
        """Проверяет, что поле ввода телефона доступно."""
        input_tel_element = self.wait_for_element('//input[@type="tel"]')
        assert input_tel_element.is_enabled(), "Поле ввода номера недоступно."
        return input_tel_element

    def reg_input_tel_symbol(self):
        """Проверяет, что поле ввода телефона не принимает символы и буквы."""
        input_tel = self.reg_input_tel()
        invalid_input = "АаZz!@#$ _"
        input_tel.send_keys(invalid_input)
        actual_value = input_tel.get_attribute('value')
        assert actual_value == "+7 ", f"Поле ввода содержит недопустимые символы: '{actual_value}'"
        self.wait_for_clickable_element('//button[text()="Получить код"]').click()

    def reg_input_tel_required(self):
        """Проверяет появление сообщения 'Обязательное поле'."""
        return self.wait_for_element('//p[text()="Обязательное поле"]')

    def reg_input_tel_symbol_limit(self):
        """Вводит 9 цифр вместо полного номера телефона."""
        input_tel = self.reg_input_tel()
        input_tel.send_keys("123456789")
        self.wait_for_clickable_element('//button[text()="Получить код"]').click()

    def reg_input_tel_part_empty(self):
        """Проверяет, что появляется сообщение 'Введите оставшиеся цифры'."""
        message_element = self.wait_for_element('//p[text()="Введите оставшиеся цифры"]')
        assert message_element.text == "Введите оставшиеся цифры", "Сообщение не совпадает с ожидаемым."
        return message_element

    def generate_random_phone(self):
        """Генерирует номер телефона в формате 9XXXXXXXXX."""
        return f"{random.randint(9000000000, 9999999999)}"

    def input_unregistered_tel(self):
        random_phone = self.generate_random_phone()
        input_tel = self.reg_input_tel()
        input_tel.send_keys(random_phone)
        self.wait_for_clickable_element('//button[text()="Получить код"]').click()

    def find_captcha(self):
        captcha_element = self.wait_for_element('//h3[text()="А вы точно не робот?"]')
        assert captcha_element.text == "А вы точно не робот?", "Неверный текст в окне капчи."
        return captcha_element