from selenium.webdriver.common.by import By
import allure
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

class RegPage:
    def __init__(self, browser):
        self.browser = browser


    def open_reg_page(self):
        try:
            with allure.step('Открыть форму регистрации'):
                self.browser.get('https://test-not-prod.kari.com/auth/reg/')
                assert 'reg' in self.browser.current_url, 'Не удалось перейти на страницу регистрации'
        except WebDriverException as e:
            allure.attach(str(e), name="Ошибка при открытии страницы", attachment_type=allure.attachment_type.TEXT)
            raise

    def select_country(self):  # Кнопка применить
        with allure.step('Подтвердить выбор страны'):
            try:
                button_submit = WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[text()="Применить"]'))
                )
                button_submit.click()
            except TimeoutException:
                allure.attach("Ошибка: Кнопка 'Применить' не стала кликабельной за 10 секунд.",
                              name="TimeoutException",
                              attachment_type=allure.attachment_type.TEXT)
                # Явно выбрасываем исключение, чтобы тест завершился как FAILED
                raise TimeoutException("Кнопка 'Применить' не стала кликабельной за 10 секунд.")


    def reg_check(self):
        try:
            with allure.step('Проверка открытия формы регистрации'):
                header_element = WebDriverWait(self.browser, 5).until(
                    EC.visibility_of_element_located((By.XPATH, '//h1'))
                )
                assert "Регистрация" in header_element.text, f"Ожидался текст 'Регистрация', но найден: {header_element.text}"
                return header_element
        except TimeoutException:
            allure.attach('Элемент не был найден на странице в течение 5 секунд', name="Ошибка при поиске элемента",
                          attachment_type=allure.attachment_type.TEXT)
            raise AssertionError("Элемент h1 не был найден на странице за 5 секунд.")


    def reg_input_tel(self):
        try:
            with allure.step('Проверка наличия поля ввода номера'):
                input_tel_element = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@type="tel"]'))
                )
                assert input_tel_element.is_enabled(), "Поле ввода номера не доступно для ввода."
                return input_tel_element
        except TimeoutException:
            allure.attach('Поле ввода номера не было найдено на странице в течение 5 секунд',
                          name="Ошибка при поиске поля ввода", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError("Поле ввода номера телефона не было найдено за 5 секунд.")


    def reg_input_tel_symbol(self):
        try:
            with allure.step('Ввести в поле ввода символы и буквы'):
                input_tel = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@type="tel"]'))
                )
                input_tel.click()
                input_tel.send_keys("АаZz!@#$ _")
                assert input_tel.get_attribute(
                    'value') == "АаZz!@#$ _", "В поле ввода не отображаются введенные символы."
                get_code_button = WebDriverWait(self.browser, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[text()="Получить код"]'))
                )
                get_code_button.click()
        except TimeoutException:
            allure.attach('Не удалось найти или кликнуть по элементам на странице',
                          name="Ошибка при взаимодействии с элементами", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError("Не удалось найти необходимые элементы (поле ввода или кнопку) в течение 5 секунд.")


    def reg_input_tel_required(self):
        try:
            with allure.step('Проверка отсутствия символов и обязательности заполнения'):
                required_message = WebDriverWait(self.browser, 5).until(
                    EC.visibility_of_element_located((By.XPATH, '//p[text()="Обязательное поле"]'))
                )
                return required_message
        except TimeoutException:
            allure.attach('Сообщение "Обязательное поле" не появилось на странице в течение 5 секунд',
                          name="Ошибка при поиске сообщения", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError('Сообщение "Обязательное поле" не появилось на странице за 5 секунд.')


    def reg_input_tel_symbol_limit(self):
        try:
            with allure.step('Ввести не полный номер'):
                input_tel = WebDriverWait(self.browser, 5).until(
                    EC.visibility_of_element_located((By.XPATH, '//input[@type="tel"]'))
                )
                input_tel.click()
                input_tel.send_keys("123456789")
                get_code_button = WebDriverWait(self.browser, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[text()="Получить код"]'))
                )
                get_code_button.click()
        except TimeoutException:
            allure.attach('Не удалось найти или кликнуть по элементам на странице в течение 5 секунд',
                          name="Ошибка при взаимодействии с элементами", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError(
                "Не удалось найти или кликнуть по элементам (поле ввода или кнопка) в течение 5 секунд.")


    def reg_input_tel_part_empty(self):
        try:
            with allure.step('Проверка кол-ва символов'):
                message_element = WebDriverWait(self.browser, 5).until(
                    EC.visibility_of_element_located((By.XPATH, '//p[text()="Введите оставшиеся цифры"]'))
                )
                assert message_element.text == "Введите оставшиеся цифры", "Сообщение на странице не совпадает с ожидаемым текстом."
                return message_element
        except TimeoutException:
            allure.attach('Сообщение "Введите оставшиеся цифры" не появилось на странице в течение 5 секунд',
                          name="Ошибка при поиске сообщения", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError('Сообщение "Введите оставшиеся цифры" не появилось на странице за 5 секунд.')


    def generate_random_phone(self):
        # Генерация номера телефона в формате +7 (9XX) XXX-XX-XX
        return f"({random.randint(900, 999)}) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"


    def input_unregistered_tel(self):
        try:
            with allure.step('Ввод незарегистрированного номера'):
                # Генерация случайного номера телефона
                random_phone = self.generate_random_phone()
                input_tel = WebDriverWait(self.browser, 5).until(
                    EC.visibility_of_element_located((By.XPATH, '//input[@type="tel"]'))
                )
                input_tel.click()
                input_tel.send_keys(random_phone)
                get_code_button = WebDriverWait(self.browser, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[text()="Получить код"]'))
                )
                get_code_button.click()
        except TimeoutException as e:
            allure.attach(str(e), name="Ошибка при поиске элемента", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError("Не удалось найти элементы на странице в течение 5 секунд.")


    def find_captcha(self):
        try:
            with allure.step('Проверка открытия окна для ввода капчи'):
                captcha_element = WebDriverWait(self.browser, 5).until(
                EC.visibility_of_element_located((By.XPATH, '//h3[text()="А вы точно не робот?"]'))
            )
            assert captcha_element.text == "А вы точно не робот?", "Неверный текст в окне капчи."
            return captcha_element
        except TimeoutException as e:
            allure.attach(str(e), name="Ошибка при поиске капчи", attachment_type=allure.attachment_type.TEXT)
            raise AssertionError("Окно для ввода капчи не было найдено в течение 10 секунд.")















