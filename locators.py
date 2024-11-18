# locators.py
from selenium.webdriver.common.by import By

class RegistrationLocators:
    CARD_TITLE = (By.ID, "card-title")
    BTN_NEW_USER = (By.ID, "kc-register")
    FIELD_NAME = (By.CSS_SELECTOR, "input[name='firstName']")
    FIELD_SURNAME = (By.CSS_SELECTOR, "input[name='lastName']")
    FIELD_EMAIL = (By.ID, "address")
    FIELD_PHONE = (By.ID, "address")
    FIELD_REGION = (By.XPATH, "//div[@class='rt-input-container rt-select__rt-input']//div[@class='rt-input__action']")
    FIELD_REGION_LIST = (By.CSS_SELECTOR, "div.rt-select__list rt-select__list--orange")
    FIELD_REGION_NAME = (By.CSS_SELECTOR, "div.rt-select__list-wrapper--rounded input[name='region'][value='520014']")
    FIELD_PASSWORD_NEW = (By.ID, "password")
    FIELD_PASSWORD = (By.ID, "password-confirm")
    FIELD_BUTTON = (By.LINK_TEXT, "Зарегистрироваться")

class AuthorizationLocators:
    CARD_TITLE = (By.ID, "card-title")
    LINK_PHONE = (By.ID, "t-btn-tab-phone")
    LINK_EMAIL = (By.ID, "t-btn-tab-mail")
    LINK_LOGIN = (By.ID, "t-btn-tab-login")
    LINK_SCORE = (By.ID, "t-btn-tab-ls")
    FIRST_PHONE = (By.ID, "username")
    FIELD_EMAIL = (By.ID, "username")
    FIELD_LOGIN = (By.ID, "username")
    FIELD_SCORE = (By.ID, "username")
    FIELD_PASSWORD = (By.ID, "password")
    FIELD_BUTTON = (By.ID, "kc-login")
    IMG_CAPTCHA_URL = (By.CSS_SELECTOR, "img.rt-captcha__image")
    FIELD_CAPTCHA = (By.ID, "captcha")