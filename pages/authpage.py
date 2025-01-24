from selenium.webdriver.common.by import By
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
import time
from pymongo import MongoClient
import string
import random

URL = 'https://test-not-prod.kari.com/auth/recovery/'

class AuthPage:

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

    def open_auth_page(self):
        try:
            with (allure.step('Открыть страницу авторизации')):
                start_time = time.time()
                self.browser.get('https://test-not-prod.kari.com/auth/')
                load_time = time.time() - start_time
                allure.attach(f"Время загрузки страницы: {load_time} секунд", name="Загрузка страницы",
                              attachment_type=allure.attachment_type.TEXT)
                assert 'auth' in self.browser.current_url, 'Не удалось открыть сайт'
                try:
                    button_submit = self.wait_for_clickable_element('//button[text()="Применить"]')
                    allure.attach("Кнопка найдена", name="Состояние кнопки",
                                  attachment_type=allure.attachment_type.TEXT)
                    button_submit.click()
                except TimeoutException:
                    allure.attach("Кнопка 'Применить' не найдена. Шаг пропущен.", name="Состояние кнопки",
                                  attachment_type=allure.attachment_type.TEXT)
        except WebDriverException as e:
            allure.attach(str(e), name="Ошибка при открытии страницы", attachment_type=allure.attachment_type.TEXT)
            raise

    def check_auth_page_elements(self):
        self.check_element_displayed('//input[@name="login"]', By.XPATH)
        self.check_element_displayed('//input[@name="password"]', By.XPATH)
        self.check_element_displayed('//button[@type="submit"]//span[text()="Войти"]', By.XPATH)
        self.check_element_displayed('//a[text()="Забыли пароль?"]', By.XPATH)
        self.check_element_displayed('//a[text()="Создать аккаунт"]', By.XPATH)
        self.check_element_displayed('//a[@href="/" and @class="css-12bp68v"]', By.XPATH)
        self.check_element_displayed('//p[text()="По СМС"]', By.XPATH)

    def click_create_button(self):
        with allure.step('Нажать "Создать аккаунт"'):
            create_button = self.wait_for_clickable_element('//a[text()="Создать аккаунт"]', By.XPATH)
            create_button.click()

    def valid_login_field(self, email, expected_error=None):
        email_field = self.wait_for_element('//input[@name="login"]', By.XPATH)
        email_field.clear()
        email_field.send_keys(email)
        login_button = self.wait_for_clickable_element('//button[@type="submit"]//span[text()="Войти"]', By.XPATH)
        login_button.click()
        if expected_error:
            error_message_element = self.wait_for_element(f"//p[contains(text(), '{expected_error}')]", By.XPATH)
            assert error_message_element.is_displayed(), f"Ошибка: Ожидалось сообщение '{expected_error}', но оно не отображается для {email}"
        else:
            try:
                # Проверка на отсутствие ошибки
                self.wait_for_element("//p[contains(text(), 'Некорректный')]", By.XPATH)
                allure.attach("Ошибка: Не должно быть сообщения об ошибке", name="Error message not found", attachment_type=allure.attachment_type.TEXT)
                raise AssertionError(f"Ошибка: Не должно быть сообщения об ошибке для {email}")
            except TimeoutException:
                # Ошибка не появилась — тест прошел успешно
                pass

    def check_auth_check(self, login, password, error=None):
        self.check_element_displayed('//input[@name="login"]', By.XPATH).send_keys(login)
        self.check_element_displayed('//input[@name="password"]', By.XPATH).send_keys(password)
        login_button = self.wait_for_clickable_element('//button[@type="submit"]//span[text()="Войти"]', By.XPATH)
        login_button.click()
        if error:
            error_message = self.wait_for_element(f'//p[contains(text(), "{error}")]', By.XPATH)
            assert error_message.is_displayed(), f"Ошибка: Ожидаемое сообщение '{error}'"
        else:
            login_success = self.wait_for_element('//p[contains(text(), "Илья")]', By.XPATH)
            assert login_success.is_displayed(), "Ошибка: Успешная авторизация не была подтверждена"

    def switch_between_login_methods(self):
        self.wait_for_element('//p[text()="По СМС"]', By.XPATH).click()
        WebDriverWait(self.browser, 10).until(lambda driver: 'sms' in driver.current_url)
        self.check_element_displayed('//input[@name="phone"]', By.XPATH)
        self.check_element_displayed('//a[@href="/" and @class="css-12bp68v"]', By.XPATH)
        self.check_element_displayed('//p[text()="Войти по номеру телефона или e-mail"]', By.XPATH)
        self.check_element_displayed('//button[text()="Получить код"]', By.XPATH)
        self.wait_for_element('//p[text()="Войти по номеру телефона или e-mail"]', By.XPATH).click()
        WebDriverWait(self.browser, 10).until(lambda driver: 'auth' in driver.current_url)

    def ya_vk_displayed(self):
        self.check_element_displayed('//div[@class="yaPersonalButtonLogo yaPersonalButtonLogo_ya"]', By.XPATH)
        self.check_element_displayed('//button[@class="e11356s31 css-14c1lv3"]', By.XPATH)

    def press_forgot_pass(self):
        self.wait_for_clickable_element('//a[text()="Забыли пароль?"]', By.XPATH).click()
        WebDriverWait(self.browser, 10).until(EC.url_to_be("https://test-not-prod.kari.com/auth/recovery/"))
        self.check_element_displayed('input[type="tel"][name="phone"]', By.CSS_SELECTOR)
        self.check_element_displayed('//a[@href="/" and @class="css-12bp68v"]', By.XPATH)
        self.check_element_displayed('//a[text()="Вход по паролю"]', By.XPATH)
        self.check_element_displayed('button.css-10vxmgq', By.CSS_SELECTOR)

    def input_reg_tel(self):
        phone_input = self.wait_for_element('input[type="tel"][name="phone"]', By.CSS_SELECTOR)
        phone_input.send_keys("9022779866")
        try:
            self.wait_for_element('p.css-1iccibi[color="error"]', By.CSS_SELECTOR)
            allure.attach("Ошибка валидации: поле подсвечено красным", name="Validation Error", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError("Поле ввода телефона подсвечено красным (ошибка валидации)")
        except TimeoutException:
            pass
        self.wait_for_element('button.css-10vxmgq', By.CSS_SELECTOR).click()

    def get_confirm_codes(phone_number: str):
        try:
            client = MongoClient('mongodb://localhost:27017/')  # Указать адрес монги
            db = client['clients']  # Выбор базы данных и коллекции
            collection = db['confirmcodes']
            query = {'phone': phone_number} # Выполнение запроса
            results = collection.find(query, {'_id': 0, 'code': 1})
            # Преобразование результатов в список
            codes = [item['code'] for item in results] # Преобразование результатов в список
            client.close() # Закрытие соединения
            return codes
        except Exception as e:
            print(f"Ошибка при подключении к MongoDB: {e}")
            return None

    def input_confirm_code(self, code):
        for i, digit in enumerate(code):
            confirm_code_field = self.wait_for_element(f"349c753b-844e-4448-a443-6edf45dee507-{i}","id")
            confirm_code_field.send_keys(digit)
        assert self.check_element_displayed('h1.css-gebv7e',By.CSS_SELECTOR,).text == "Восстановление пароля", "Форма восстановления пароля не найдена"
        assert self.check_element_displayed('input[name="password"]',By.CSS_SELECTOR), "Поле ввода пароля не найдено"
        assert self.check_element_displayed('input[name="confirmPassword"]',By.CSS_SELECTOR), "Поле подтверждения пароля не найдено"
        assert self.check_element_displayed('button.css-10vxmgq',By.CSS_SELECTOR), "Кнопка 'Изменить и войти' не найдена"

    def generate_password(self):
        characters = string.ascii_letters + string.digits
        while True:
            password = ''.join(random.choices(characters, k=8))
            if (any(c.isdigit() for c in password) and
                    any(c.isupper() for c in password)):
                return password

    def change_password(self):
        new_password = self.generate_password()
        password_field = self.wait_for_element('input[name="password"]',By.CSS_SELECTOR)
        password_field.send_keys(new_password)
        confirm_password_field = self.wait_for_element('input[name="confirmPassword"]',By.CSS_SELECTOR)
        confirm_password_field.send_keys(new_password)
        error_messages = self.browser.find_elements(By.CSS_SELECTOR, 'p.css-1iccibi[color="error"]')
        assert not error_messages, "Ошибка: обнаружены сообщения о ненадежном пароле"
        submit_button = self.wait_for_element('button.css-10vxmgq',By.CSS_SELECTOR)
        submit_button.click()
        login_success = self.wait_for_element('//p[contains(text(), "Илья")]', By.XPATH)
        assert login_success.is_displayed(), "Ошибка: Успешная авторизация не была подтверждена"


