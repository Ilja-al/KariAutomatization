from selenium.webdriver.common.by import By
import allure
import random

class RegPage:
    def __init__(self, browser):
        self.browser = browser

    def open_reg_page(self):
        with allure.step('Открыть форму регистрации'):
            self.browser.get('https://test-not-prod.kari.com/auth/reg/')

    def click_button_submit(self):
        with allure.step('Подтвердить выбор страны'):
            button_submit = self.browser.find_element(By.XPATH, '//button[text()="Применить"]')
            button_submit.click()

    def reg_check(self):
        with allure.step('Проверка открытия формы регистрации'):
            return self.browser.find_element(By.XPATH, '//h1')

    def reg_input_tel(self):
        with allure.step('Проверка наличия поля ввода номера'):
            return self.browser.find_element(By.XPATH, '//input[@type="tel"]')

    def reg_input_tel_symbol(self):
        with allure.step('Ввести в поле ввода символы и буквы'):
            input_tel = self.browser.find_element(By.XPATH, '//input[@type="tel"]')
            input_tel.click()
            input_tel.send_keys("АаZz!@#$ _")
            get_code_button = self.browser.find_element(By.XPATH,'//button[text()="Получить код"]')
            get_code_button.click()

    def reg_input_tel_required(self):
        with allure.step('Проверка отсутствия символов и обязательности заполнения'):
            return self.browser.find_element(By.XPATH,'//p[text()="Обязательное поле"]')

    def reg_input_tel_symbol_limit(self):
        with allure.step('Ввести не полный номер'):
            input_tel = self.browser.find_element(By.XPATH, '//input[@type="tel"]')
            input_tel.click()
            input_tel.send_keys("123456789")
            get_code_button = self.browser.find_element(By.XPATH,'//button[text()="Получить код"]')
            get_code_button.click()

    def reg_input_tel_part_empty(self):
        with allure.step('Проверка кол-ва символов'):
            return self.browser.find_element (By.XPATH, '//p[text()="Введите оставшиеся цифры"]')

    # Функция для генерации случайного номера телефона
    def generate_random_phone(self):
        # Генерация номера телефона в формате +7 (XXX) XXX-XX-XX
        return f"({random.randint(900, 999)}) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"

    def input_unregistered_tel(self):
        with allure.step('Ввод незарегистрированного номера'):
            random_phone = self.generate_random_phone()
            input_tel = self.browser.find_element(By.XPATH, '//input[@type="tel"]')
            input_tel.click()
            input_tel.send_keys(random_phone)
            get_code_button = self.browser.find_element(By.XPATH, '//button[text()="Получить код"]')
            get_code_button.click()

    def find_captcha(self):
        with allure.step('Проверка открытия окна для ввода капчи'):
            return self.browser.find_element(By.XPATH, '//h3[text()="А вы точно не робот?"]')















