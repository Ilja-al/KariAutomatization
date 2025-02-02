from selenium.webdriver.common.by import By
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:

    # Локаторы элементов
    LOGIN_ICON_LOCATOR = '//button[@class="css-1svjifm e2cllgv3"]'  # Иконка входа
    ENTER_REGISTRATION_BUTTON_LOCATOR = '//a[@class="css-oc613h e1bfq77c24"]'  # Кнопка "Войти или зарегистрироваться"

    def __init__(self, browser):
        self.browser = browser

    # Метод для открытия главной страницы
    def open_main_page(self, url):
        with allure.step('Открыть главную страницу'):
            print(f"Попытка открыть сайт: {url}")
            self.browser.get(url)
            # Проверяем, что загруженный URL совпадает с ожидаемым
            WebDriverWait(self.browser, 30).until(
                EC.url_to_be(url)
            )
            if url != self.browser.current_url:
                raise AssertionError(f"Ошибка: Ожидался URL: {url}, но фактический URL: {self.browser.current_url}")
            else:
                print(f"Сайт успешно открыт: {self.browser.current_url}")

   def click_login_icon(self): # Иконка входа
    with allure.step('Нажать иконку входа'):
        print("Поиск иконки")    
        login_icon = self.wait_for_clickable_element('//button[@class="css-1svjifm e2cllgv3"]')
        print("Нажатие на иконку")    
        login_icon.click()

def click_enter_registration(self): # войти или зарегистрироваться
    with allure.step('Нажать "Войти или зарегистрироваться"'):
        print("Поиск кнопки Войти")     
        enter_registration = self.wait_for_clickable_element('//a[@class="css-oc613h e1bfq77c24"]')
        print("Нажатие кнопки Войти")  
        enter_registration.click()

    # Общий метод для ожидания и проверки видимости элемента
    def check_and_wait_for_element(self, locator, by=By.XPATH, timeout=60):
        element = WebDriverWait(self.browser, timeout).until(
            EC.visibility_of_element_located((by, locator))
        )
        assert element.is_displayed(), f"Элемент {locator} не отображается"
        return element

    # Метод для ожидания наличия элемента (работает с CSS и XPath)
    def wait_for_element(self, locator, by=By.XPATH, timeout=60):
        return WebDriverWait(self.browser, timeout).until(
            EC.presence_of_element_located((by, locator))
        )

    # Метод для ожидания кликабельности элемента
    def wait_for_clickable_element(self, locator, by=By.XPATH, timeout=60):
        return WebDriverWait(self.browser, timeout).until(
            EC.element_to_be_clickable((by, locator))
        )
