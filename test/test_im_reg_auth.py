from pages.mainpage import MainPage
from pages.authpage import AuthPage
from pages.regpage import RegPage
import allure

@allure.feature('Registration. Go to the form new account data')
@allure.story('Click button "Create acc"')
def test_reg_form_check(browser):
    main_page = MainPage(browser)
    main_page.open_main_page()
    main_page.select_country()
    main_page.click_login_icon()
    main_page.click_enter_registration()
    main_page_auth = AuthPage(browser)
    main_page_auth.click_create_button()
    main_page_auth_reg = RegPage(browser)
    assert main_page_auth_reg.reg_check().is_displayed()

@allure.feature('Registration. Go to the form new account data')
@allure.story('Click button "Create acc"')
def test_reg_form_input_tel(browser):
    auth_reg = RegPage(browser)
    auth_reg.open_reg_page()
    auth_reg.select_country()
    assert auth_reg.reg_input_tel().is_displayed()

@allure.feature('Registration. Go to the form new account data')
@allure.story('Click button "Create acc"')
def test_reg_form_input_tel_symbol(browser):
    auth_reg = RegPage(browser)
    auth_reg.open_reg_page()
    auth_reg.select_country()
    auth_reg.reg_input_tel_symbol()
    assert auth_reg.reg_input_tel_required().is_displayed()

@allure.feature('Registration. Go to the form new account data')
@allure.story('Click button "Create acc"')
def test_reg_from_input_tel_symbol_limit(browser):
    auth_reg = RegPage(browser)
    auth_reg.open_reg_page()
    auth_reg.select_country()
    auth_reg.reg_input_tel_symbol_limit()
    assert auth_reg.reg_input_tel_part_empty().is_displayed()

@allure.feature('Registration. Go to the form new account data')
@allure.story('Input_unregistered_tel')
def test_input_unregistered_tel(browser):
    auth_reg = RegPage(browser)
    auth_reg.open_reg_page()
    auth_reg.select_country()
    auth_reg.input_unregistered_tel()
    assert auth_reg.find_captcha().is_displayed()

@allure.feature('Auth. Validation fields')
@allure.story('Auth. Validation fields')
def test_auth_valid_fields(browser):
    auth_page = AuthPage(browser)
    auth_page.open_auth_page()
    auth_page.select_country()
    auth_page.test_invalid_email_login()
























