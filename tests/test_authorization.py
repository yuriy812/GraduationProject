import pytest
import json
import requests
import easyocr
import csv
import os
import time
import pandas as pd
from datetime import datetime
from settings import url
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import AuthorizationLocators, RegistrationLocators

# Глобальный список для хранения результатов
results = []
def save_results(results):
    if not results:
        print("Нет результатов для сохранения.")
        return

    report_dir = 'reports'

    # Создание директории, если она не существует
    os.makedirs(report_dir, exist_ok=True)

    csv_path = os.path.join(report_dir, 'test_report.csv')

    try:
        # Сохранение результатов в формате CSV
        with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['test', 'status', 'error', 'timestamp'])
            writer.writeheader()
            writer.writerows(results)

        print(f"Отчет успешно сохранен в {csv_path}")
    except Exception as e:
        print(f"Ошибка при сохранении отчета: {e}")

# Функция для загрузки данных из JSON
def load_test_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


# Загрузка данных
test_data = load_test_data('test_data.json')


# Функция для обработки капчи
def handle_captcha(driver):
    img_path = None  # Инициализируем img_path как None
    try:
        # Проверяем, есть ли элемент капчи
        captcha_present = False
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(AuthorizationLocators.IMG_CAPTCHA_URL)
            )
            captcha_present = True
        except:
            print("Капча не обнаружена, продолжаем вход без капчи.")

        if captcha_present:
            element_phone = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(AuthorizationLocators.LINK_PHONE)
            )
            element_phone.click()

            # Получаем URL изображения капчи
            url_img = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located(AuthorizationLocators.IMG_CAPTCHA_URL)
            ).get_attribute("src")

            if not url_img:
                print("Не удалось получить URL капчи")
                return None

            # Создаем папку для сохранения изображения
            img_dir = 'images'
            os.makedirs(img_dir, exist_ok=True)

            # Сохраняем изображение на диск
            img_path = os.path.join(img_dir, 'captcha_image.jpg')
            print("Получение ссылки на изображение капчи...")

            # Добавление заголовка User-Agent
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6598.117 Safari/537.36'
            }
            response = requests.get(url_img, headers=headers)

            # Проверка успешности запроса и сохранение
            if response.status_code == 200:
                with open(img_path, 'wb') as img_file:
                    img_file.write(response.content)
                print("Изображение сохранено.")
            else:
                print(f"Ошибка при получении капчи: {response.status_code}")
                return None

            # Создание объекта OCR reader
            reader = easyocr.Reader(['en'])
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
            captcha_input.click()
            captcha_input.send_keys(captcha)

            # Проверка правильности введенной капчи
            if not is_captcha_correct(driver):
                raise ValueError("Капча не прошла проверку")

        else:
            # Логика продолжения ввода данных без капчи
            print("Ввод данных без капчи")
            # Здесь вы можете добавить код для ввода других тестовых данных

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        take_screenshot(driver)  # Создание скриншота при ошибке

    finally:
        # Удаление файла изображения, если он существует
        if img_path and os.path.exists(img_path):  # Проверяем, что img_path не None
            os.remove(img_path)
            print(f"Файл {img_path} удален.")


# Вспомогательная функция для проверки правильности капчи
def is_captcha_correct(driver):
    # Здесь следует добавить логику проверки:
    # например, можно проверить наличие элемента с сообщением об ошибке
    try:
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(RegistrationLocators.ERROR_MESSAGE)
        )
        # Предполагается, что сообщение об ошибке должно быть на странице
        return "Неверно введен текст с картинки" not in error_message.text
    except Exception:
        return True  # Предполагаем, что нет ошибок, если нет сообщений об ошибках


# Вспомогательная функция для создания скриншота
def take_screenshot(driver):
    timestamp = int(time.time())
    screenshot_filename = os.path.join('images', f'result_{timestamp}.jpg')
    driver.save_screenshot(screenshot_filename)  # Используем метод save_screenshot
    print(f"Создан скриншот: {screenshot_filename}")


# Функция для выполнения авторизации

def perform_login(driver, password):
    if password:
        try:
            # Находим поле для ввода пароля и вводим его
            password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(AuthorizationLocators.FIELD_PASSWORD)
            )
            password_input.send_keys(password)

            # Нажимаем кнопку входа в систему
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(AuthorizationLocators.FIELD_BUTTON)
            )
            login_button.click()

            # Проверка успешной авторизации
            success_account = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(RegistrationLocators.PERSONAL_ACCOUNT)
            )
            assert "Личный кабинет" in success_account.text, "Переход в личный кабинет не отображается"

            # Проверка, что сообщений об ошибках больше нет
            try:
                error_message = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located(RegistrationLocators.ERROR_MESSAGE)
                )
                assert "Неверный логин или пароль" not in error_message.text, "Сообщение об ошибке отображается неожиданно"
            except TimeoutException:
                # Если сообщения об ошибке не найдено, просто продолжаем
                pass


        except Exception as e:
            # Создание скриншота при ошибке
            take_screenshot(driver)
            print(f"Ошибка при выполнении входа: {e}")
            raise  # Повторно выбрасываем исключение, если нужно

        # Добавление результата в список
        results.append({'test': 'Login Test', 'status': 'Passed', 'timestamp': datetime.now()})
    else:
        results.append(
            {'test': 'Login Test', 'status': 'Failed', 'error': 'No password provided', 'timestamp': datetime.now()})
    print(f"Текущие результаты: {results}")


def save_results(results):
    if not results:
        print("Нет результатов для сохранения.")
        return

        # Создание DataFrame из результатов
    df = pd.DataFrame(results)
    report_dir = 'reports'

    # Создание директории, если она не существует
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    excel_path = os.path.join(report_dir, 'test_report.xlsx')

    try:
        df.to_excel(excel_path, index=False)
        print(f"Отчет успешно сохранен в {excel_path}")
    except Exception as e:
        print(f"Ошибка при сохранении отчета: {e}")


def pytest_sessionfinish(session, exitstatus):
    save_results(results)

@pytest.mark.parametrize("user_data", test_data["valid"])
def test_authorization_email(setup_chrome, user_data):
    driver = setup_chrome
    driver.get(url)

    email_click = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.LINK_EMAIL)
    )
    email_click.click()
    # Вызов функции обработки капчи
    handle_captcha(driver)
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.FIELD_EMAIL)
    )
    email_input.send_keys(user_data['email'])

    perform_login(driver, user_data['password'])


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

    # Вызов функции обработки капчи

    perform_login(driver, user_data['password'])







