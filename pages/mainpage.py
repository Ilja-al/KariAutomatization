from selenium.webdriver.common.by import By
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

class MainPage:

    def __init__(self, browser):
        self.browser = browser

    def open_main_page(self): # Открытие главной страницы
        with allure.step('Открыть сайт'):
            self.browser.get('https://test-not-prod.kari.com/')


    def close_modal(self):
        with allure.step('Закрытие модалки выбора страны'):
            try:
                close_modal = self.browser.find_element((By.XPATH, '//div[@class="css-1bfagdg"]'))
                ActionChains(self.browser).move_to_element(close_modal).click().perform()
            except TimeoutException:
                print("Ошибка при закрытии модального окна")


    def click_button_submit(self): # Кнопка применить
        with allure.step('Подтвердить выбор страны'):
            try:
                button_submit = WebDriverWait(self.browser, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[text()="Применить"]'))
                )
                button_submit.click()
            except TimeoutException:
                print("Ошибка: Кнопка 'Применить' не стала кликабельной за 10 секунд.")


    def click_login_icon(self): # Иконка входа
        with allure.step('Нажать иконку входа'):
            try:
                login_icon = WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@class="css-1svjifm e2cllgv3"]'))
                )
                login_icon.click()
            except TimeoutException:
                print("Ошибка: Иконка входа не стала кликабельной за 10 секунд.")

    def click_enter_registration(self): # войти или зарегистрироваться
        with allure.step('Нажать "Войти или зарегистрироваться"'):
            try:
                enter_registration = WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//a[@class="css-oc613h e1bfq77c24"]'))
                )
                enter_registration.click()
            except TimeoutException:
                print("Ошибка: Ссылка 'Войти или зарегистрироваться' не стала кликабельной за 10 секунд.")