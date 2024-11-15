# locators.py
from selenium.webdriver.common.by import By

class RegistrationLocators:
    CARD_TITLE = (By.ID, "card-title")
    BTN_NEW_USER = (By.ID, "kc-register")
    FIELD_NAME = (By.CSS_SELECTOR, "input[name='firstName']")