from selenium.webdriver.common.by import By
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class AuthPage:

    def __init__(self, browser):
        self.browser = browser


    def click_create_button(self): # кнопка "Создать аккаунт"
        with allure.step('Нажать "Создать аккаунт"'):
            try:
                create_button = WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//a[text()="Создать аккаунт"]'))
                )
                create_button.click()
            except TimeoutException:
                print('Ошибка: Кнопка "Создать аккаунт" не стала кликабельной за 10 секунд.')