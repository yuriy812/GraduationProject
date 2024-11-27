# registration.py
import pytest
import json
import datetime
from module_report import results, save_results
from module_screenshot import take_screenshot  # Убедитесь, что у вас есть эта функция
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from settings import url
from locators import *  # Импортируем локаторы


# Функция для загрузки данных из JSON
def load_test_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


test_data = load_test_data('test_data.json')

results = []  # Список для хранения результатов тестов

def perform_login(driver):
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    # Ожидаем, пока элемент с ID "card-title" станет доступным
    element = wait.until(EC.presence_of_element_located(RegistrationLocators.CARD_TITLE))

    # Проверяем, что текст элемента содержит "Авторизация"
    assert "Авторизация" in element.text, "Текст элемента не содержит 'Авторизация'"

    # Нажимаем на кнопку "Зарегистрироваться"
    btn_new_user = wait.until(EC.element_to_be_clickable(RegistrationLocators.BTN_NEW_USER))
    btn_new_user.click()

    # Ожидаем, пока элемент с ID "card-title" станет доступным после перехода на страницу регистрации
    element = wait.until(EC.presence_of_element_located(RegistrationLocators.CARD_TITLE))

    # Проверяем, что текст элемента содержит "Регистрация"
    assert "Регистрация" in element.text, "Текст элемента не содержит 'Регистрация'"


def fill_registration_form(driver, user_data):
    wait = WebDriverWait(driver, 10)

    if user_data['username']:
        field_name = wait.until(EC.presence_of_element_located(RegistrationLocators.FIELD_NAME))
        field_name.send_keys(user_data['username'])

    if user_data['user_surname']:
        field_user_surname = wait.until(EC.presence_of_element_located(RegistrationLocators.FIELD_SURNAME))
        field_user_surname.send_keys(user_data['user_surname'])

    if user_data['email']:
        field_email = wait.until(EC.presence_of_element_located(RegistrationLocators.FIELD_EMAIL))
        field_email.send_keys(user_data['email'])

    if user_data['password']:
        field_password_new = wait.until(EC.presence_of_element_located(RegistrationLocators.FIELD_PASSWORD_NEW))
        field_password_new.send_keys(user_data['password'])

        field_password = wait.until(EC.presence_of_element_located(RegistrationLocators.FIELD_PASSWORD))
        field_password.send_keys(user_data['password'])

    field_button = wait.until(EC.element_to_be_clickable(RegistrationLocators.FIELD_BUTTON))
    field_button.click()


@pytest.mark.parametrize("user_data", test_data["valid"])
def test_registration_valid(setup_chrome, user_data):
    driver = setup_chrome
    perform_login(driver)

    try:
        fill_registration_form(driver, user_data)

        # Проверка успешной регистрации
        success_account = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(RegistrationLocators.PERSONAL_ACCOUNT)
        )
        assert "Личный кабинет" in success_account.text, "Переход в личный кабинет не отображается"

        # Проверка, что сообщение об ошибке не отображается
        try:
            error_message = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located(RegistrationLocators.ERROR_MESSAGE)
            )
            assert "Неверный логин или пароль" not in error_message.text, "Сообщение об ошибке отображается неожиданно"
        except TimeoutException:
            pass  # Сообщение об ошибке не отображается

            # Сохранение результатов теста
        results.append({
            'test': 'Registration Valid Test',
            'status': 'Passed',
            'timestamp': datetime.now(),
            'error': None
        })


    except Exception as e:
        take_screenshot(driver)  # Сохраняем скриншот при ошибке
        print(f"Ошибка при выполнении регистрации: {e}")
        results.append({
            'test': 'Registration Valid Test',
            'status': 'Failed',
            'timestamp': datetime.now(),
            'error': str(e)
        })
        raise  # Повторно выбрасываем исключение, если нужно


@pytest.mark.parametrize("user_data", test_data["invalid"])
def test_registration_invalid(setup_chrome, user_data):
    driver = setup_chrome
    perform_login(driver)
    fill_registration_form(driver, user_data)

    try:
        # Проверка ошибок
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(RegistrationLocators.ERROR_MESSAGE)
        )
        assert error_message.is_displayed(), "Сообщение об ошибке не отображается"
        assert "Учётная запись уже существует" in error_message.text, "Сообщение об ошибке не содержит 'Учётная запись уже существует'"

        # Сохранение результатов теста
        results.append({
            'test': 'Registration Invalid Test',
            'status': 'Passed',
            'timestamp': datetime.now(),
            'error': None
        })

    except Exception as e:
        take_screenshot(driver)  # Сохраняем скриншот при ошибке
        print(f"Ошибка при выполнении регистрации: {e}")
        results.append({
            'test': 'Registration Invalid Test',
            'status': 'Failed',
            'timestamp': datetime.now(),
            'error': str(e)
        })
        raise  # Повторно выбрасываем исключение, если нужно
    finally:
        save_results(results)  # Сохранение результатов после выполнения теста
        print(f"Текущие результаты: {results}")