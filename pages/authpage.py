import pytest
from selenium.webdriver.common.by import By
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import WebDriverException
import time

class AuthPage:

    def __init__(self, browser):
        self.browser = browser

    def open_auth_page(self):
        try:
            with allure.step('Открыть страницу авторизации'):
                start_time = time.time()
                self.browser.get('https://test-not-prod.kari.com/auth/')
                load_time = time.time() - start_time
                allure.attach(f"Время загрузки страницы: {load_time} секунд", name="Загрузка страницы",
                              attachment_type=allure.attachment_type.TEXT)
                assert 'auth' in self.browser.current_url, 'Не удалось открыть сайт'
                try:
                    button_submit = WebDriverWait(self.browser, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//button[text()="Применить"]'))
                    )
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
        try:
            email_field = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@name="login"]'))
            )
            assert email_field.is_displayed(), "Поле 'Телефон/E-mail' не отображается"
            password_field = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@name="password"]'))
            )
            assert password_field.is_displayed(), "Поле 'Пароль' не отображается"
            login_button = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]//span[text()="Войти"]'))
            )
            assert login_button.is_displayed(), "Кнопка 'Войти' не отображается"
            forgot_password_button = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a[text()="Забыли пароль?"]'))
            )
            assert forgot_password_button.is_displayed(), "Кнопка 'Забыли пароль' не отображается"
            create_account_button = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a[text()="Создать аккаунт"]'))
            )
            assert create_account_button.is_displayed(), "Кнопка 'Создать аккаунт' не отображается"
            close_button = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//a[@href="/" and @class="css-12bp68v"]'))
            )
            assert close_button.is_displayed(), "Крест для закрытия не отображается"
            sms_button = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//p[text()="По СМС"]'))
            )
            assert sms_button.is_displayed(), "Кнопка 'По СМС' не отображается"
        except Exception as e:
            raise AssertionError(f"Ошибка при проверке элементов: {str(e)}")


    def click_create_button(self): # кнопка "Создать аккаунт"
        with allure.step('Нажать "Создать аккаунт"'):
            try:
                create_button = WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//a[text()="Создать аккаунт"]'))
                )
                create_button.click()
            except TimeoutException:
                print('Ошибка: Кнопка "Создать аккаунт" не стала кликабельной за 10 секунд.')


    def valid_login_field(self, email, expected_error=None):
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
            if expected_error:
                error_message_element = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, f"//p[contains(text(), '{expected_error}')]")
                    )
                )
                assert error_message_element.is_displayed(), f"Ошибка: Ожидалось сообщение '{expected_error}', но оно не отображается для {email}"
            else:
                # Проверка на отсутствие ошибки
                try:
                    # Ожидаем, что сообщение об ошибке не появится
                    error_message_element = WebDriverWait(self.browser, 5).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//p[contains(text(), 'Некорректный')]")
                        )
                    )
                    assert not error_message_element.is_displayed(), f"Ошибка: Не должно быть сообщения об ошибке для {email}"
                except TimeoutException:
                    # Ошибка не должна была появиться, тест прошел успешно
                    pass
        except TimeoutException:
            allure.attach(
                f"Ошибка: Сообщение о некорректном вводе данных не отображается для {email}. Ожидалось сообщение: '{expected_error}'",
                name="TimeoutException",
                attachment_type=allure.attachment_type.TEXT)
            raise TimeoutException(
                f"Сообщение о некорректном вводе данных не отображается для {email}. Ожидалось сообщение: '{expected_error}'")



    def check_auth_check(self, login, password, error=None):
        email_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="login"]'))
        )
        email_field.clear()
        email_field.send_keys(login)
        password_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="password"]'))
        )
        password_field.clear()
        password_field.send_keys(password)
        login_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]//span[text()="Войти"]'))
        )
        login_button.click()
        if error:
            try:
                # Ожидаем появления сообщения об ошибке
                error_message = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, f'//p[contains(text(), "{error}")]')
                    )
                )
                assert error_message.is_displayed(), f"Ошибка: Ожидалось сообщение '{error}'"
            except TimeoutException:
                allure.attach(f"Ожидаемое сообщение об ошибке '{error}' не появилось",
                              name="Error message not found",
                              attachment_type=allure.attachment_type.TEXT)
                raise
        else:
            try:
                # Проверяем успешную авторизацию
                login_success = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//p[contains(text(), "Илья")]')
                    )
                )
                assert login_success.is_displayed(), "Ошибка: Успешная авторизация не была подтверждена"
            except TimeoutException:
                allure.attach("Ошибка: Сообщение о успешной авторизации не появилось",
                              name="Success message not found",
                              attachment_type=allure.attachment_type.TEXT)
                raise

    def switch_between_login_methods(self):
        bySMS = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//p[text()="По СМС"]')))
        bySMS.click()
        assert 'sms' in self.browser.current_url, 'Не удалось перейти на форму входа по СМС'
        phone_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="phone"]')))
        assert phone_field.is_displayed(), "Поле 'Телефон' не отображается"
        close_button = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="/" and @class="css-12bp68v"]')))
        assert close_button.is_displayed(), "Крест для закрытия не отображается"
        phone_email_button = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//p[text()="Войти по номеру телефона или e-mail"]')))
        assert phone_email_button.is_displayed(), "Кнопка 'Войти по номеру телефона или e-mail' не отображается"
        get_code_button = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[text()="Получить код"]')))
        assert get_code_button.is_displayed(), "Кнопка 'Получить код' не отображается"
        phone_email_button.click()
        # проверяем только факт перехода, т.к. остальное проверено ранее
        assert 'auth' in self.browser.current_url, 'Не удалось перейти на форму входа по логину и пароль'
        close_button.click()
        expected_url = "https://test-not-prod.kari.com/"
        WebDriverWait(self.browser, 10).until(
            lambda driver: driver.current_url == expected_url) # Ожидаем, что URL будет изменен на ожидаемый
        assert expected_url == self.browser.current_url, 'Не удалось перейти на форму входа по логину и пароль'


    def ya_vk_displayed(self):
        ya_button = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@class="yaPersonalButtonLogo yaPersonalButtonLogo_ya"]')))
        assert ya_button.is_displayed(), "Кнопка 'Яндекс' не отображается"
        vk_button = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//button[@class="e11356s31 css-14c1lv3"]')))
        assert vk_button.is_displayed(), "Кнопка 'VK' не отображается"

