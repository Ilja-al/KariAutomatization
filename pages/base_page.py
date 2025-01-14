from selenium.webdriver.common.by import By
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:

    def __init__(self, browser):
        self.browser = browser

    def click_button_submit(self): # Кнопка применить
        with allure.step('Подтвердить выбор страны'):
            try:
                button_submit = WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[text()="Применить"]'))
                )
                button_submit.click()
            except TimeoutException:
                print("Ошибка: Кнопка 'Применить' не стала кликабельной за 10 секунд.")