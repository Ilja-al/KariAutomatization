from selenium.webdriver.common.by import By
import allure

class MainPage:

    def __init__(self, browser):
        self.browser = browser

    def open_main_page(self): # открытие главной страницы
        with allure.step('Открыть сайт'):
            self.browser.get('https://test-not-prod.kari.com/')

    def click_button_submit(self): # кнопка применить
        with allure.step('Подтвердить выбор страны'):
            button_submit = self.browser.find_element(By.XPATH, '//button[text()="Применить"]')
            button_submit.click()

    def click_login_icon(self): # иконка входа
        with allure.step('Нажать иконку входа'):
            login_icon = self.browser.find_element(By.XPATH, '//*[@class="user"]')
            login_icon.click()

    def click_enter_registration(self): # войти или зарегистрироваться
        with allure.step('Нажать "Войти или зарегистрироваться"'):
            enter_registration = self.browser.find_element(By.XPATH, '//*[@class="css-oc613h e1bfq77c24"]')
            enter_registration.click()