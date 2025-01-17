import pytest
from selenium.webdriver.common.by import By
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

class AuthPage:

    def __init__(self, browser):
        self.browser = browser


    def open_auth_page(self):
        try:
            with allure.step('Открыть страницу авторизации'):
                self.browser.get('https://test-not-prod.kari.com/auth/')
            assert 'aut' in self.browser.current_url, 'Не удалось перейти на страницу авторизации'
        except WebDriverException as e:
            allure.attach(str(e), name="Ошибка при открытии страницы", attachment_type=allure.attachment_type.TEXT)
            raise

    def select_country(self): # Кнопка применить
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


    def click_create_button(self): # кнопка "Создать аккаунт"
        with allure.step('Нажать "Создать аккаунт"'):
            try:
                create_button = WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//a[text()="Создать аккаунт"]'))
                )
                create_button.click()
            except TimeoutException:
                print('Ошибка: Кнопка "Создать аккаунт" не стала кликабельной за 10 секунд.')

    @pytest.mark.parametrize("email, expected_error", [
        ('privet@g', 'Некорректный E-mail'),
        ('798888', 'Некорректный E-mail'),
        (',./*"(*?).', 'Некорректный E-mail')
    ])
    def test_invalid_email_login(self, email, expected_error):
        try:
                email_field = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@name="login"]'))
                )
                email_field.clear()
                email_field.send_keys(email)
                login_button = WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]//span[text()="Войти"]'))
                )
                login_button.click()
                error_message_element = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//p[@class='css-1iccibi' and text()='Некорректный E-mail']"))
                )
                assert error_message_element.is_displayed(), f"Ошибка: {expected_error} не отображается"
        except TimeoutException:
            allure.attach("Ошибка: Сообщение о некорректном E-mail не отображается.",
                          name="TimeoutException",
                          attachment_type=allure.attachment_type.TEXT)
            # Явно выбрасываем исключение, чтобы тест завершился как FAILED
            raise TimeoutException("Сообщение о некорректном E-mail не отображается")


