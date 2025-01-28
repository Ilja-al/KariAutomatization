from pages.mainpage import MainPage
from pages.authpage import AuthPage
from pages.regpage import RegPage
import allure
import pytest


@allure.story('1.Регистрация. Переход к форме заполнения данных нового аккаунта')
@allure.title('Нажать кнопку "Создать аккаунт"')
def test_reg_form_check(browser): #Нажать кнопку "Создать аккаунт"
    main_page = MainPage(browser)
    main_page.open_main_page()
    main_page.click_login_icon()
    main_page.click_enter_registration()
    main_page_auth = AuthPage(browser)
    main_page_auth.click_create_button()


@allure.story('1.Регистрация. Переход к форме заполнения данных нового аккаунта')
@allure.title('Ввести в поле ввода номера символы и буквы')
@pytest.mark.parametrize("phone, error", [
        ('АаZz!@#$ _', 'Обязательное поле'),
        ('987654321', 'Введите оставшиеся цифры')])
def test_reg_form_input_tel_validation(browser, phone, error):
    auth_reg = RegPage(browser)
    auth_reg.open_reg_page()
    auth_reg.reg_input_tel_validation(phone, error)


@allure.story('1.Регистрация. Переход к форме заполнения данных нового аккаунта')
@allure.title('Ввести номер телефона не зарегистрированного пользователя и нажать "Получить код"')
def test_input_unregistered_tel(browser):
    auth_reg = RegPage(browser)
    auth_reg.open_reg_page()
    auth_reg.input_unregistered_tel()
    assert auth_reg.find_captcha().is_displayed()


@allure.story('1.Регистрация. Переход к форме заполнения данных нового аккаунта')
@allure.title('Ввести номер телефона зарегестрированного пользователя и нажать кнопку "Получить код"')
def test_reg_form_input_tel(browser):
    auth_reg = RegPage(browser)
    auth_reg.open_reg_page()
    auth_reg.reg_input_tel()
    assert auth_reg.find_captcha().is_displayed()


@allure.story('2.Авторизация. Валидация поля Телефон/E-mail')
@allure.title('Ввод различных данных в поле логина и проверка валидации')
@pytest.mark.parametrize("email, expected_error", [
        ('tests@example.com',''),
        ('79022779866',''),
        ('798888', 'Некорректный номер телефона'),
        (',./*"(*?).', 'Введите свой телефон или e-mail'),
        ('privet@g', 'Некорректный E-mail')
    ])
def test_auth_valid_login_field(browser, email, expected_error):
    auth_page = AuthPage(browser)
    auth_page.open_auth_page()
    auth_page.check_auth_page_elements()
    auth_page.valid_login_field(email, expected_error)


@allure.story('3.Авторизация. Проверка авторизации')
@allure.title('Ввод различных данных и проверка авторизации ')
@pytest.mark.parametrize("login, password, error", [
        ('79112223388', 'PolkA890!', 'Неверный логин или пароль'),
        ('79000000000', 'PolkA890!', 'Неверный логин или пароль'),
        ('79022779866', 'PolkA890!', '')
    ])
def test_auth_check_auth(browser, login, password, error):
    auth_page = AuthPage(browser)
    auth_page.open_auth_page()
    auth_page.check_auth_check(login, password, error)


@allure.story('4.Авторизация. Проверка переключения между способами входа')
@allure.title('Авторизация. Проверка переключения между способами входа')
def test_switch_between_login_methods(browser):
    auth_page = AuthPage(browser)
    auth_page.open_auth_page()
    auth_page.switch_between_login_methods()

@allure.story('5.Авторизация по SMS. Проверка валидации')
@allure.title('Авторизация по SMS. Проверка валидации')
@pytest.mark.parametrize("phone, error", [
        ('790227798', 'Введите оставшиеся цифры'),
        ('79022779866', '')])
def test_auth_sms_valid_phone_field(browser, phone, error):
    auth_page = AuthPage(browser)
    auth_page.open_auth_page()
    auth_page.auth_sms_valid_phone_field(phone, error)


@allure.story('6.Yandex и ВК ID. Отображение кнопок входа')
@allure.title('Yandex и ВК ID. Отображение кнопок входа')
def test_ya_vk_displayed(browser):
    auth_page = AuthPage(browser)
    auth_page.open_auth_page()
    auth_page.ya_vk_displayed()


@allure.story('7.Восстановление пароля пользователя')
@allure.title('Восстановление пароля пользователя')
def test_password_recovery(browser, mongo_client):
    phone_number = "9022779866"
    auth_page = AuthPage(browser)
    auth_page.open_auth_page()
    auth_page.press_forgot_pass()
    auth_page.input_reg_tel(phone_number)
    auth_page.enter_sms_code(phone_number, mongo_client)
    auth_page.change_password()
