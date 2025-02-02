import allure
import pytest
from pages.mainpage import MainPage
#from pages.auth_page import AuthPage  # Предполагаю, что у вас есть такой класс для работы со страницей авторизации/регистрации


@allure.story('1.Регистрация. Переход к форме заполнения данных нового аккаунта')
@allure.title('Нажать кнопку "Создать аккаунт"')
@pytest.mark.usefixtures("browser")
def test_reg_form_check(browser):  # Нажать кнопку "Создать аккаунт"
    main_page = MainPage(browser)
    #auth_page = AuthPage(browser)

    main_page.open_main_page("https://yourwebsite.com")  # Замените на актуальный URL вашего сайта
    main_page.click_login_icon()
    main_page.click_enter_registration()
    auth_page.click_create_button()

'''
    @allure.story('1.Регистрация. Переход к форме заполнения данных нового аккаунта')
    @allure.title('Ввести в поле ввода номера символы и буквы')
    @pytest.mark.parametrize("phone, error", [
            ('АаZz!@#$ _', 'Обязательное поле'),
            ('987654321', 'Введите оставшиеся цифры')])
    def test_reg_form_input_tel_validation(self, phone, error):
        self.reg_page.open_reg_page()
        self.reg_page.reg_input_tel_validation(phone, error)


    @allure.story('1.Регистрация. Переход к форме заполнения данных нового аккаунта')
    @allure.title('Ввести номер телефона не зарегистрированного пользователя и нажать "Получить код"')
    def test_input_unregistered_tel(self):
        self.reg_page.open_reg_page()
        self.reg_page.input_unregistered_tel()
        assert self.reg_page.find_captcha().is_displayed()


    @allure.story('1.Регистрация. Переход к форме заполнения данных нового аккаунта')
    @allure.title('Ввести номер телефона зарегестрированного пользователя и нажать кнопку "Получить код"')
    def test_reg_form_input_tel(self): #поправить, на случай если код отправляется без капчи, либо чаще раза в минуту
        self.reg_page.open_reg_page()
        self.reg_page.reg_input_tel()
        assert self.reg_page.find_captcha().is_displayed()


    @allure.story('2.Авторизация. Валидация поля Телефон/E-mail')
    @allure.title('Ввод различных данных в поле логина и проверка валидации')
    @pytest.mark.parametrize("email, expected_error", [
            ('tests@example.com',''),
            ('79022779866',''),
            ('798888', 'Некорректный номер телефона'),
            (',./*"(*?).', 'Введите свой телефон или e-mail'),
            ('privet@g', 'Некорректный E-mail')
        ])
    def test_auth_valid_login_field(self, email, expected_error):
        self.auth_page.open_auth_page()
        self.auth_page.check_auth_page_elements()
        self.auth_page.valid_login_field(email, expected_error)


    @allure.story('3.Авторизация. Проверка авторизации')
    @allure.title('Ввод различных данных и проверка авторизации ')
    @pytest.mark.parametrize("login, password, error", [
            ('79112223388', 'PolkA890!', 'Неверный логин или пароль'),
            ('79000000000', 'PolkA890!', 'Неверный логин или пароль'),
            ('79935229866', 'PolkA890!', '')
        ])
    def test_auth_check_auth(self, login, password, error):
        self.auth_page.open_auth_page()
        self.auth_page.check_auth_check(login, password, error)


    @allure.story('4.Авторизация. Проверка переключения между способами входа')
    @allure.title('Авторизация. Проверка переключения между способами входа')
    def test_switch_between_login_methods(self):
        self.auth_page.open_auth_page()
        self.auth_page.switch_between_login_methods()


    @allure.story('5.Авторизация по SMS. Проверка валидации')
    @allure.title('Авторизация по SMS. Проверка валидации')
    @pytest.mark.parametrize("phone, error", [
            ('790227798', 'Введите оставшиеся цифры'),
            ('79022779866', '')])
    def test_auth_sms_valid_phone_field(self, phone, error):
        self.auth_page.open_auth_page()
        self.auth_page.auth_sms_valid_phone_field(phone, error)


    @allure.story('6.Yandex и ВК ID. Отображение кнопок входа')
    @allure.title('Yandex и ВК ID. Отображение кнопок входа')
    def test_ya_vk_displayed(self): #поправить, не ожидается загрузка ya, ток проверяется наличие элемента
        self.auth_page.open_auth_page()
        self.auth_page.ya_vk_displayed()


    @allure.story('7.Восстановление пароля пользователя')
    @allure.title('Восстановление пароля пользователя')
    def test_password_recovery(self, mongo_client):
        phone_number = "9022779866"
        self.auth_page.open_auth_page()
        self.auth_page.press_forgot_pass()
        self.auth_page.input_reg_tel(phone_number)
        self.auth_page.enter_sms_code(phone_number, mongo_client)
        self.auth_page.change_password()
'''
