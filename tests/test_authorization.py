# test_authorization.py
import pytest
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By  # Не забудьте импортировать By
from settings import url
from locators import AuthorizationLocators  # Импортируем локаторы


# Функция для загрузки данных из JSON
def load_test_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

    # Загрузка данных


test_data = load_test_data('test_data.json')


# Параметризация тестов с использованием валидных данных
@pytest.mark.parametrize("user_data", test_data["valid"])
def test_authorization_page(setup_chrome, user_data):
    driver = setup_chrome
    driver.get(url)

    # Ожидаем, пока элемент с ID "card-title" станет доступным
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.CARD_TITLE)
    )

    # Проверяем, что текст элемента содержит "Авторизация"
    assert "Авторизация" in element.text, "Текст элемента не содержит 'Авторизация'"

    element_email = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(AuthorizationLocators.LINK_EMAIL)
    )
    element_email.click()

    # Step 1: Locate the email input field and enter the email
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.FIELD_EMAIL)
    )
    email_input.click()
    email_input.send_keys(user_data['email'])

    # Step 2: Locate the password input field and enter the password
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.FIELD_PASSWORD)
    )
    password_input.click()
    password_input.send_keys(user_data['password'])

    # Step 3: Locate and click the login button
    login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.BTN_NEW_USER)
    )
    login_button.click()

    # Step 5: Assert that the user is redirected to the dashboard or home page
    WebDriverWait(driver, 10).until(
        EC.title_contains("Dashboard"))  # Ожидаем, что заголовок страницы содержит "Dashboard"
    assert driver.current_url == "https://example.com/dashboard"  # Замените на фактический URL после входа

    # Step 6: Optionally, check for a logout button or user profile element to confirm successful login
    assert WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@id='logout']"))
    )  # Убедитесь, что элемент для выхода доступен

    driver.quit()  # Закрываем драйвер после теста
