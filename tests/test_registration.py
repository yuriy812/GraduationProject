# test_registration.py
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import url, nev_name
from locators import RegistrationLocators  # Импортируем локаторы
import time

def test_authorization(setup_chrome):
    driver = setup_chrome
    driver.get(url)

    # Ожидаем, пока элемент с ID "card-title" станет доступным
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(RegistrationLocators.CARD_TITLE)
    )

    # Проверяем, что текст элемента содержит "Авторизация"
    assert "Авторизация" in element.text, "Текст элемента не содержит 'Авторизация'"

    # Нажимаем на кнопку "Зарегистрироваться"
    wait = WebDriverWait(driver, 10)
    btn_newuser = wait.until(EC.element_to_be_clickable(RegistrationLocators.BTN_NEW_USER))
    btn_newuser.click()

    # Ожидаем, пока элемент с ID "card-title" станет доступным после перехода на страницу регистрации
    element = wait.until(EC.presence_of_element_located(RegistrationLocators.CARD_TITLE))

    # Проверяем, что текст элемента содержит "Регистрация"
    assert "Регистрация" in element.text, "Текст элемента не содержит 'Регистрация'"

    # Добавляем имя
    field_name = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(RegistrationLocators.FIELD_NAME)
    )
    field_name.click()
    field_name.send_keys(nev_name)

    # Проверяем введенное имя
    entered_name = field_name.get_attribute('value')

    if entered_name == nev_name:
        # Сохранение скриншота
        timestamp = int(time.time())
        screenshot_filename = f'images/result_{timestamp}.png'
        driver.save_screenshot(screenshot_filename)
        print(f'Screenshot saved as: {screenshot_filename}')
    else:
        raise Exception("Login error: Введенное имя не совпадает с ожидаемым.")



    @pytest.mark.parametrize("data", [
        {"username": "validUser1", "email": "valid@example.com", "password": "pass123"},
        {"username": "validUser2", "email": "another@example.com", "password": "pass456"}
    ])
    def test_registration_valid(data):
        # Логика успешной регистрации
        assert data['username']
        assert '@' in data['email']
        assert len(data['password']) > 0

    def test_registration_invalid(test_data):
        for data in test_data['invalid']:
            # Логика обработки невалидных значений
            error_count = 0
            if not data['username']:
                error_count += 1  # Ожидаем ошибку при пустом имени пользователя
            if "@" not in data['email']:
                error_count += 1  # Ожидаем ошибку при невалидном email
            if not data['password']:
                error_count += 1  # Ожидаем ошибку при пустом пароле
            assert error_count > 0  # Ожидаем, что будет хотя бы одна ошибка