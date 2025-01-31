from selenium.webdriver.common.by import By
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import string
import random
import time
from config.links import Links
from base.base_page import BasePage

class AuthPage(BasePage):

    # Метод для ожидания наличия элемента (работает с CSS и XPath)
    def wait_for_element(self, locator, by=By.XPATH, timeout=15):
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

    # Метод для закрытия браузера (для стабильности и избежания утечки
    def close_browser(self):
        if self.browser:
            self.browser.quit()

    def open_auth_page(self):
        with (allure.step('Открыть страницу авторизации')):
            page_url = Links.AUTH_PAGE
            self.browser.get(page_url)
            assert page_url in self.browser.current_url, 'Не удалось открыть сайт'
            button_submit = self.wait_for_clickable_element('//button[text()="Применить"]')
            button_submit.click()

    def check_auth_page_elements(self):
        with allure.step('Проверка наличия необходимых элементов на странице'):
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
        with allure.step('Проверка открытия страницы регистрации'):
            self.check_element_displayed('//h1[text()="Регистрация"]', By.XPATH)


    def valid_login_field(self, email, expected_error=None): #перепроверить
        with allure.step('Проверка наличия поля ввода логина'):
            email_field = self.wait_for_element('//input[@name="login"]', By.XPATH)
        with allure.step('Очистка поля ввода логина'):
            email_field.clear()
        with allure.step('Заполнить поле (значения указаны в параметризации)'):
            email_field.send_keys(email)
        with allure.step('Нажать кнопку "Войти"'):
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
        with allure.step('Ввести логин и пароль (значения указаны в параметризации)'):
            self.check_element_displayed('//input[@name="login"]', By.XPATH).send_keys(login)
            self.check_element_displayed('//input[@name="password"]', By.XPATH).send_keys(password)
        with allure.step('Нажать кнопку "Войти"'):
            login_button = self.wait_for_clickable_element('//button[@type="submit"]//span[text()="Войти"]', By.XPATH)
            login_button.click()
        with allure.step('Проверка успешной авторизации'):
            if error:
                error_message = self.wait_for_element(f'//p[contains(text(), "{error}")]', By.XPATH)
                assert error_message.is_displayed(), f"Ошибка: Ожидаемое сообщение '{error}'"
            else:
                login_success = self.wait_for_element('//p[contains(text(), "Илья")]', By.XPATH)
                assert login_success.is_displayed(), "Ошибка: Успешная авторизация не была подтверждена"

    def switch_between_login_methods(self):
        with allure.step('Нажать кнопку "По СМС"'):
            self.wait_for_element('//p[text()="По СМС"]', By.XPATH).click()
        with allure.step('Проверка изменения способа входа'):
            WebDriverWait(self.browser, 10).until(lambda driver: 'sms' in driver.current_url)
        with allure.step('Проверка отображения необходимых элементов'):
            self.check_element_displayed('//input[@name="phone"]', By.XPATH)
            self.check_element_displayed('//a[@href="/" and @class="css-12bp68v"]', By.XPATH)
            self.check_element_displayed('//p[text()="Войти по номеру телефона или e-mail"]', By.XPATH)
            self.check_element_displayed('//button[text()="Получить код"]', By.XPATH)
        with allure.step('Нажать кнопку "Войти по номеру телефона или e-mail"'):
            self.wait_for_element('//p[text()="Войти по номеру телефона или e-mail"]', By.XPATH).click()
        with allure.step('Проверка изменения способа входа на предыдущий'):
            WebDriverWait(self.browser, 10).until(lambda driver: 'auth' in driver.current_url)

    def auth_sms_valid_phone_field(self, phone, expected_error=None):
        with allure.step('Нажать кнопку "По СМС"'):
            For_SMS = self.wait_for_element('//p[text()="По СМС"]', By.XPATH)
            For_SMS.click()
        with allure.step('Очистка поля ввода номера'):
            phone_filed = self.wait_for_element('//input[@name="phone"]', By.XPATH)
            phone_filed.clear()
        with allure.step('Ввести телефон (значения указаны в параметризации)'):
            phone_filed.send_keys(phone)
        with allure.step('Нажать кнопку "Получить код"'):
            self.wait_for_clickable_element('//button[text()="Получить код"]', By.XPATH).click()
        with allure.step('Проверка наличия ошибки валидации'):
            if expected_error:
                error_message_element = self.wait_for_element(f"//p[contains(text(), '{expected_error}')]", By.XPATH)
                assert error_message_element.is_displayed(), f"Ошибка: Ожидалось сообщение '{expected_error}', но оно не отображается для {phone}"
            else:
                try:
                    # Проверка на отсутствие ошибки
                    self.wait_for_element("//p[contains(text(), 'оставшиеся')]", By.XPATH)
                    allure.attach("Ошибка: Не должно быть сообщения об ошибке", name="Error message not found",
                                  attachment_type=allure.attachment_type.TEXT)
                    raise AssertionError(f"Ошибка: Не должно быть сообщения об ошибке для {phone}")
                except TimeoutException:
                    # Ошибка не появилась — тест прошел успешно
                    pass

    def ya_vk_displayed(self):
        with allure.step('Проверка отображения кнопок Яндекса и ВК'):
            # Ожидание появления iframe и переключение на него
            iframe = self.wait_for_element('//iframe[@id="iframe"]', By.XPATH)
            self.browser.switch_to.frame(iframe)
            # Ожидание появления кнопки Яндекса
            self.wait_for_element('//div[contains(@class, "yaPersonalButtonLogo")]', By.XPATH)
            # Ожидание появления кнопки ВК
            self.wait_for_element('//button[contains(@class, "css-14c1lv3")]', By.XPATH)
            # Возвращаемся в основной контекст страницы
            self.browser.switch_to.default_content()

    def press_forgot_pass(self):
        with allure.step('Нажать "Забыли пароль?"'):
            self.wait_for_clickable_element('//a[text()="Забыли пароль?"]', By.XPATH).click()
        with allure.step('Проверка перехода на форму и отображения элементов'):
            WebDriverWait(self.browser, 10).until(EC.url_to_be("https://test-not-prod.kari.com/auth/recovery/?redirection="))
            self.check_element_displayed('input[type="tel"][name="phone"]', By.CSS_SELECTOR)
            self.check_element_displayed('//a[@href="/" and @class="css-12bp68v"]', By.XPATH)
            self.check_element_displayed('//a[text()="Вход по паролю"]', By.XPATH)
            self.check_element_displayed('button.css-10vxmgq', By.CSS_SELECTOR)

    def input_reg_tel(self, phone_number):
        with allure.step('Ввод номера телефона'):
            phone_input = self.wait_for_element('input[type="tel"][name="phone"]', By.CSS_SELECTOR)
            phone_input.send_keys(phone_number)
        with allure.step('Проверка отсутствия ошибок валидации'):
            try:
                self.wait_for_element('p.css-1iccibi[color="error"]', By.CSS_SELECTOR)
                allure.attach("Ошибка валидации: поле подсвечено красным", name="Validation Error", attachment_type=allure.attachment_type.TEXT)
                raise AssertionError("Поле ввода телефона подсвечено красным (ошибка валидации)")
            except TimeoutException:
                pass

    def enter_sms_code(self, phone_number, mongo_client):
        try:
            # Подключение к MongoDB
            confirmcodes_collection = mongo_client["confirmcodes"]
            clients_collection = mongo_client["clients"]
            # Формируем запрос для удаления объекта из confirmcodes
            query = {"phone": f"+7{phone_number}"}
            deleted_count = confirmcodes_collection.delete_one(query).deleted_count
            if deleted_count:
                print(f"Объект с телефоном +7{phone_number} успешно удален из MongoDB (confirmcodes).")
            else:
                print(f"Объект с телефоном +7{phone_number} не найден в MongoDB (confirmcodes).")
            with allure.step('Нажать "Получить код"'):
                submit_button = self.wait_for_clickable_element("//button[text()='Получить код']", By.XPATH)
                submit_button.click()
            # Небольшая задержка для генерации кода
            time.sleep(2)
            # Повторно запрашиваем данные из clients
            projection = {"oneTimePassword.confirmCode": 1, "_id": 0}
            result = clients_collection.find_one(query, projection)
            if not result or "oneTimePassword" not in result or "confirmCode" not in result["oneTimePassword"]:
                raise ValueError("Не удалось найти код подтверждения в базе данных (clients)!")
            confirm_code = result["oneTimePassword"]["confirmCode"]
            with allure.step('Ввод кода подтверждения'):
                # Ввод каждой цифры кода в соответствующий input[data-id]
                for i, digit in enumerate(confirm_code):
                    code_input = self.wait_for_element(f"input[data-id='{i}']", By.CSS_SELECTOR)
                    code_input.send_keys(digit)
                print("Код подтверждения успешно введен!")
            with allure.step('Проверка открытия формы и отображения элементов'):
                assert self.check_element_displayed('h1.css-gebv7e', By.CSS_SELECTOR).text == "Восстановление пароля", "Форма восстановления пароля не найдена"
                assert self.check_element_displayed('input[name="password"]', By.CSS_SELECTOR), "Поле ввода пароля не найдено"
                assert self.check_element_displayed('input[name="confirmPassword"]', By.CSS_SELECTOR), "Поле подтверждения пароля не найдено"
                assert self.check_element_displayed('button.css-10vxmgq', By.CSS_SELECTOR), "Кнопка 'Изменить и войти' не найдена"
                print("Все элементы формы восстановления пароля успешно найдены!")
        except Exception as e:
            print(f"Что-то пошло не так: {e}")

    def generate_password(self, length=8):
        characters = string.ascii_letters + string.digits
        while True:
            password = ''.join(random.choices(characters, k=length))
            if (any(c.isdigit() for c in password) and any(c.isupper() for c in password)):
                return password

    def change_password(self):
        with allure.step('Генерация нового пароля'):
            new_password = self.generate_password()
        with allure.step('Ввод нового пароля'):
            password_field = self.wait_for_element('input[name="password"]', By.CSS_SELECTOR)
            password_field.clear()
            password_field.send_keys(new_password)
        with allure.step('Ввод подтверждения пароля'):
            confirm_password_field = self.wait_for_element('input[name="confirmPassword"]', By.CSS_SELECTOR)
            confirm_password_field.clear()
            confirm_password_field.send_keys(new_password)
        with allure.step('Проверка наличия сообщений об ошибках'):
            error_messages = self.browser.find_elements(By.CSS_SELECTOR, 'p.css-1iccibi[color="error"]')
            assert not error_messages, f"Ошибка: обнаружены сообщения о ненадежном пароле: {error_messages}"
        with allure.step('Нажать "Изменить и войти"'):
            submit_button = self.wait_for_element('button.css-10vxmgq', By.CSS_SELECTOR)
            submit_button.click()
        with allure.step('Проверка успешного входа'):
            login_success = self.wait_for_element('//p[contains(text(), "Илья")]', By.XPATH)
            assert login_success.is_displayed(), "Ошибка: Успешная авторизация не была подтверждена"
        with allure.step('Выход из аккаунта'):
            profile_element = self.wait_for_clickable_element('p.css-jjvis4.e2cllgv0', By.CSS_SELECTOR)
            profile_element.click()
            logout_button = self.wait_for_clickable_element('button.e1bfq77c14.css-23bvf4', By.CSS_SELECTOR)
            logout_button.click()
        with allure.step('Открытие формы входа'):
            login_icon = self.wait_for_clickable_element('//button[@class="css-1svjifm e2cllgv3"]', By.XPATH)
            login_icon.click()
        with allure.step('Нажать войти или зарегистрироваться'):
            enter_registration = self.wait_for_clickable_element('//a[@class="css-oc613h e1bfq77c24"]', By.XPATH)
            enter_registration.click()
        with allure.step('Ввод логина и измененного пароля'):
            login_field = self.check_element_displayed('//input[@name="login"]', By.XPATH)
            login_field.clear()
            login_field.send_keys('+79022779866')
            password_field = self.check_element_displayed('//input[@name="password"]', By.XPATH)
            password_field.clear()
            password_field.send_keys(new_password)
        with allure.step('Нажать "Войти"'):
            login_button = self.wait_for_clickable_element('//button[@type="submit"]//span[text()="Войти"]', By.XPATH)
            login_button.click()
        with allure.step('Повторная проверка успешного входа'):
            assert login_success, "Ошибка: Повторная авторизация не была подтверждена"
