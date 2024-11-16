# locators.py
from selenium.webdriver.common.by import By

class RegistrationLocators:
    CARD_TITLE = (By.ID, "card-title")
    BTN_NEW_USER = (By.ID, "kc-register")
    FIELD_NAME = (By.CSS_SELECTOR, "input[name='firstName']")
    FIELD_SURNAME = (By.CSS_SELECTOR, "input[name='lastName']")
    FIELD_EMAIL = (By.ID, "address")
    FIELD_PHONE = (By.ID, "address")
    FIELD_REGION = (By.CSS_SELECTOR, "div.rt-input__action[css='1']")
    FIELD_REGION_NAME = (By.CSS_SELECTOR, "div.rt-select__list-wrapper--rounded input[type='hidden'][name='region'][value='5200050']")
    FIELD_PASSWORD_NEW = (By.ID, "password")
    FIELD_PASSWORD = (By.ID, "password-confirm")
    FIELD_BUTTON = (By.LINK_TEXT, "Зарегистрироваться")

class AuthorizationLocators:
    LINK_PHONE = (By.ID, "t-btn-tab-phone']")
    LINK_EMAIL = (By.ID, "t-btn-tab-mail']")
    LINK_LOGIN = (By.ID, "t-btn-tab-login']")
    LINK_SCORE = (By.ID, "t-btn-tab-ls")
    FIRST_PHONE = (By.ID, "username")
    FIELD_EMAIL = (By.ID, "username")
    FIELD_LOGIN = (By.ID, "username")
    FIELD_SCORE = (By.ID, "username")
    FIELD_PASSWORD = (By.ID, "password")
    BTN_NEW_USER = (By.ID, "kc-login")