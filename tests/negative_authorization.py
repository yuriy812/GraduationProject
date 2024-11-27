import pytest
import json
import requests
import easyocr
import time
from settings import url
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import *
from module_report import *

# Глобальный список для хранения результатов тестов
results = []


# Функция для загрузки данных из JSON
def load_test_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


# Загрузка данных
test_data = load_test_data('test_data.json')


# Функция для обработки капчи
def handle_captcha(driver):
    img_path = None
    try:
        # Проверяем наличие капчи
        captcha_present = is_captcha_present(driver)

        if captcha_present:
            element_phone = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(AuthorizationLocators.LINK_PHONE)
            )
            element_phone.click()

            img_path = download_captcha_image(driver)
            captcha = recognize_captcha(img_path)

            # Ввод капчи в поле
            enter_captcha(driver, captcha)

            # Проверяем правильность введенной капчи
            if not is_captcha_correct(driver):
                raise ValueError("Капча не прошла проверку")
        else:
            print("Ввод данных без капчи")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        take_screenshot(driver)
    finally:
        cleanup_image(img_path)


def is_captcha_present(driver):
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(AuthorizationLocators.IMG_CAPTCHA_URL)
        )
        return True
    except TimeoutException:
        return False


def download_captcha_image(driver):
    url_img = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(AuthorizationLocators.IMG_CAPTCHA_URL)
    ).get_attribute("src")

    img_dir = 'images'
    os.makedirs(img_dir, exist_ok=True)
    img_path = os.path.join(img_dir, 'captcha_image.jpg')

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6598.117 Safari/537.36'
    }
    response = requests.get(url_img, headers=headers)

    if response.status_code == 200:
        with open(img_path, 'wb') as img_file:
            img_file.write(response.content)
        print("Изображение сохранено.")
        return img_path
    else:
        print(f"Ошибка при получении капчи: {response.status_code}")
        return None


def recognize_captcha(img_path):
    if img_path:
        reader = easyocr.Reader(['en'])
        result = reader.readtext(img_path, beamWidth=5, text_threshold=0.5)
        if result:
            return result[0][1]  # Берем первый распознанный текст
        else:
            raise ValueError("Капча не распознана")
    return None


def enter_captcha(driver, captcha):
    captcha_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.FIELD_CAPTCHA)
    )
    captcha_input.click()
    captcha_input.send_keys(captcha)


def cleanup_image(img_path):
    if img_path and os.path.exists(img_path):
        os.remove(img_path)
        print(f"Файл {img_path} удален.")


def is_captcha_correct(driver):
    try:
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(RegistrationLocators.ERROR_MESSAGE)
        )
        return "Неверно введен текст с картинки" not in error_message.text
    except TimeoutException:
        return True


def take_screenshot(driver):
    timestamp = int(time.time())
    screenshot_filename = os.path.join('images', f'result_{timestamp}.jpg')
    driver.save_screenshot(screenshot_filename)
    print(f"Создан скриншот: {screenshot_filename}")


def negative_perform_login(driver, password):
    if password:
        try:
            password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(AuthorizationLocators.FIELD_PASSWORD)
            )
            password_input.send_keys(password)

            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(AuthorizationLocators.FIELD_BUTTON)
            )
            login_button.click()

            success_account = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(RegistrationLocators.PERSONAL_ACCOUNT)
            )
            assert "Личный кабинет" in success_account.text, "Переход в личный кабинет не отображается"

            try:
                error_message = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located(RegistrationLocators.ERROR_MESSAGE)
                )
                assert "Неверный логин или пароль" not in error_message.text, "Сообщение об ошибке отображается неожиданно"
            except TimeoutException:
                pass
                # Добавление результата в список
            results.append({'test': 'Login Test', 'status': 'Passed', 'timestamp': datetime.now()})
        except Exception as e:
                # Создание скриншота при ошибке
                take_screenshot(driver)
                print(f"Ошибка при выполнении входа: {e}")
                results.append({'test': 'Login Test', 'status': 'Failed', 'error': str(e), 'timestamp': datetime.now()})
                raise  # Повторно выбрасываем исключение, если нужно
    else:
        results.append(
            {'test': 'Login Test', 'status': 'Failed', 'error': 'No password provided',
                     'timestamp': datetime.now()})

        print(f"Текущие результаты: {results}")
        save_results(results)


@pytest.mark.parametrize("user_data", test_data["invalid"])
def test_authorization_phone_invalid(setup_chrome, user_data):
    driver = setup_chrome
    driver.get(url)

    phone_click = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.LINK_PHONE)
    )
    phone_click.click()

    handle_captcha(driver)

    phone_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.FIRST_PHONE)
    )
    phone_input.send_keys(user_data['phone'])

    negative_perform_login(driver, user_data['password'])
@pytest.mark.parametrize("user_data", test_data["invalid"])
def test_authorization_email_invalid(setup_chrome, user_data):
    driver = setup_chrome
    driver.get(url)

    email_click = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.LINK_EMAIL)
    )
    email_click.click()

    handle_captcha(driver)

    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.FIELD_EMAIL)
    )
    email_input.send_keys(user_data['email'])

    negative_perform_login(driver, user_data['password'])
@pytest.mark.parametrize("user_data", test_data["invalid"])
def test_authorization_login_invalid(setup_chrome, user_data):
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

    negative_perform_login(driver, user_data['password'])
@pytest.mark.parametrize("user_data", test_data["invalid"])
def test_negative_authorization_score_invalid(setup_chrome, user_data):
    driver = setup_chrome
    driver.get(url)

    score_click = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.LINK_SCORE)
    )
    score_click.click()
    # Вызов функции обработки капчи
    handle_captcha(driver)
    score_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(AuthorizationLocators.FIELD_SCORE)
    )
    score_input.send_keys(user_data['score'])

    negative_perform_login(driver, None, user_data['password'])  # Передаем None для имени пользователя


