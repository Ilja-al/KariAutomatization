from selenium.webdriver.common.by import By
import allure

class AuthPage:

    def __init__(self, browser):
        self.browser = browser

    def click_create_button(self): # кнопка "Создать аккаунт"
        with allure.step('Нажать "Создать аккаунт"'):
            create_button = self.browser.find_element(By.XPATH, '//*[@class="css-9fd0nx"]')
            create_button.click()