from pages.mainpage import MainPage
from pages.authpage import AuthPage
from pages.regpage import RegPage
import allure
import pytest

@allure.feature('ИМ - Регистрация/авторизация')
@allure.story('Регистрация. Переход к форме заполнения данных нового аккаунта')
@allure.title('Нажать кнопку "Создать аккаунт"')
def test_reg_form_check(browser):
    main_page = MainPage(browser)
    main_page.open_main_page()
    main_page.click_login_icon()
    main_page.click_enter_registration()
    main_page_auth = AuthPage(browser)
    main_page_auth.click_create_button()
    main_page_auth_reg = RegPage(browser)
    assert main_page_auth_reg.reg_check().is_displayed()

@allure.feature('ИМ - Регистрация/авторизация')
@allure.story('Регистрация. Переход к форме заполнения данных нового аккаунта')
@allure.title('Ввести в поле ввода номера символы и буквы')
def test_reg_form_input_tel_symbol(browser):
    auth_reg = RegPage(browser)
    auth_reg.open_reg_page()
    auth_reg.reg_input_tel_symbol()
    assert auth_reg.reg_input_tel_required().is_displayed()

@allure.feature('ИМ - Регистрация/авторизация')
@allure.story('Регистрация. Переход к форме заполнения данных нового аккаунта')
@allure.title('Ввести в поле ввода номера недостаточное кол-во символов')
def test_reg_from_input_tel_symbol_limit(browser):
    auth_reg = RegPage(browser)
    auth_reg.open_reg_page()
    auth_reg.reg_input_tel_symbol_limit()
    assert auth_reg.reg_input_tel_part_empty().is_displayed()

@allure.feature('ИМ - Регистрация/авторизация')
@allure.story('Регистрация. Переход к форме заполнения данных нового аккаунта')
@allure.title('Ввести номер телефона незарегестрированного пользователя и нажать кнопку "Получить код"')
def test_input_unregistered_tel(browser):
    auth_reg = RegPage(browser)
    auth_reg.open_reg_page()
    auth_reg.input_unregistered_tel()
    assert auth_reg.find_captcha().is_displayed()

@allure.feature('ИМ - Регистрация/авторизация')
@allure.story('Регистрация. Переход к форме заполнения данных нового аккаунта"')
@allure.title('Ввести номер телефона зарегестрированного пользователя и нажать кнопку "Получить код"')
def test_reg_form_input_tel(browser):
    auth_reg = RegPage(browser)
    auth_reg.open_reg_page()
    assert auth_reg.reg_input_tel().is_displayed()

@allure.feature('ИМ - Регистрация/авторизация')
@allure.story('Авторизация. Валидация поля Телефон/E-mail')
@allure.title('Ввод различных данных в поле логина и проверка валидации')
@pytest.mark.parametrize("email, expected_error", [
        ('test@example.com',''),
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


@allure.feature('ИМ - Регистрация/авторизация')
@allure.story('Авторизация. Проверка авторизации.')
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


@allure.feature('ИМ - Регистрация/авторизация')
@allure.story('Авторизация. Проверка переключения между способами входа.')
@allure.title('Авторизация. Проверка переключения между способами входа.')
def test_switch_between_login_methods(browser):
    auth_page = AuthPage(browser)
    auth_page.open_auth_page()
    auth_page.switch_between_login_methods()

@allure.feature('ИМ - Регистрация/авторизация')
@allure.story('Yandex и ВК ID. Отображение кнопок входа')
@allure.title('Yandex и ВК ID. Отображение кнопок входа')
def test_ya_vk_displayed(browser):
    auth_page = AuthPage(browser)
    auth_page.open_auth_page()


def test_password_recovery(browser):
    auth_page = AuthPage(browser)
    auth_page.open_auth_page()
    auth_page.press_forgot_pass()
    auth_page.input_reg_tel()

































