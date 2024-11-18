import pytest
import json
import requests
import easyocr
import os
from settings import url
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from locators import AuthorizationLocators


# Функция для загрузки данных из JSON
def load_test_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


# Загрузка данных
test_data = load_test_data('test_data.json')


# Функция для выполнения авторизации
def perform_login(setup_chrome):
    driver = setup_chrome
    driver.get(url)
    driver.refresh()
    # Ожидаем, пока элемент с ID "card-title" станет доступным
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.CARD_TITLE)
    )
    # Проверяем, что текст элемента содержит "Авторизация"
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.CARD_TITLE)
    )
    assert "Авторизация" in element.text, "Текст элемента не содержит 'Авторизация'"

    # Клик по элементу, чтобы загрузить капчу
    element_phone = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.LINK_PHONE)
    )
    element_phone.click()

    # Получаем URL изображения капчи
    url_img = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(AuthorizationLocators.IMG_CAPTCHA_URL)
    ).get_attribute("src")  # Получаем атрибут src изображения

    # Создаем папку для сохранения изображения
    img_dir = 'images'
    os.makedirs(img_dir, exist_ok=True)

    # Сохраняем изображение на диск
    img_path = os.path.join(img_dir, 'image.jpg')
    response = requests.get(url_img)
    with open(img_path, 'wb') as img_file:
        img_file.write(response.content)

    # Создание объекта OCR reader
    reader = easyocr.Reader(['en'])  # Поддержка английского и русского языков

    # Чтение текста с изображения
    result = reader.readtext(img_path, beamWidth=5, text_threshold=0.5)

    # Извлечение текста капчи
    captcha = ''
    if result:
        captcha = result[0][1]  # Берем первый распознанный текст
    else:
        raise ValueError("Капча не распознана")

    # Ввод капчи в поле
    captcha_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.FIELD_CAPTCHA)
    )
    captcha_input.send_keys(captcha)

    # Удаление файла изображения
    os.remove(img_path)


@pytest.mark.parametrize("user_data", test_data["valid"])
def test_authorization_phone(setup_chrome, user_data):
    driver = setup_chrome
    driver.get(url)
    phone_click = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.LINK_PHONE)
    )
    phone_click.click()
    # Вводим данные для авторизации
    phone_click = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.FIRST_PHONE)
    )
    phone_click.click()
    phone_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.FIRST_PHONE)
    )
    phone_input.send_keys(user_data['phone'])

    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.FIELD_PASSWORD)
    )
    password_input.click()
    password_input.send_keys(user_data['password'])

    # Нажимаем кнопку входа в систему
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(AuthorizationLocators.FIELD_BUTTON)
    )
    login_button.click()
    # Параметризация тестов с использованием валидных данных


@pytest.mark.parametrize("user_data", test_data["valid"])
def test_authorization_email(setup_chrome, user_data):
    driver = setup_chrome
    driver.get(url)
    driver.refresh()
    email_click = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.LINK_EMAIL)
    )
    email_click.click()
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.FIELD_EMAIL)
    )
    email_input.send_keys(user_data['email'])
    # Нажимаем кнопку входа в систему
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(AuthorizationLocators.FIELD_BUTTON)
    )
    login_button.click()
    # Дополнительные проверки после входа могут быть добавлены здесь
    # driver.quit()  # Закрываем драйвер после теста


@pytest.mark.parametrize("user_data", test_data["valid"])
def test_authorization_login(setup_chrome, user_data):
    driver = setup_chrome
    driver.get(url)
    login_click = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.LINK_LOGIN)
    )
    login_click.click()

    login_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.FIELD_LOGIN)
    )
    login_input.send_keys(user_data['login'])
    # Нажимаем кнопку входа в систему
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(AuthorizationLocators.FIELD_BUTTON)
    )
    login_button.click()
    # Дополнительные проверки после входа могут быть добавлены здесь
    # driver.quit()  # Закрываем драйвер после теста


@pytest.mark.parametrize("user_data", test_data["valid"])
def test_authorization_score(setup_chrome, user_data):
    driver = setup_chrome
    driver.get(url)
    score_click = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.LINK_SCORE)
    )
    score_click.click()
    score_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.FIELD_SCORE)
    )
    score_input.send_keys(user_data['login'])
    # Нажимаем кнопку входа в систему
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(AuthorizationLocators.FIELD_BUTTON)
    )
    login_button.click()
    # Дополнительные проверки после входа могут быть добавлены здесь
    driver.quit()  # Закрываем драйвер после теста
