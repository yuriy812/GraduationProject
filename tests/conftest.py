# conftest.py
import os
from dotenv import load_dotenv
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from settings import url, valid_email  # Предполагается, что url уже загружен из настроек

# Загрузка переменных окружения
load_dotenv()


@pytest.fixture
def chrome_options():
    options = Options()
    # options.add_argument('--headless')  # Запуск без графического интерфейса, если нужно
    options.add_argument('-foreground')  # Запуск в переднем плане
    return options


@pytest.fixture
def setup_chrome(chrome_options):
    # Получаем путь до драйвера из переменных окружения
    driver_path = os.getenv("EDGEDRIVER_PATH")
    if not driver_path:
        raise ValueError("Переменная окружения EDGEDRIVER_PATH не установлена.")

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_window_size(1440, 900)  # Установка размера окна
    yield driver  # Передаем драйвер в тесты
    driver.quit()  # Закрываем драйвер после выполнения тестов


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # Эта функция помогает обнаружить, что какой-либо тест не прошел успешно
    # и передать эту информацию в teardown:
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture
def web_browser(setup_chrome):
    return setup_chrome


def test_example(web_browser):
    # Проверяем, что переменная url действительно установлена
    if url is None:
        raise ValueError("Переменная окружения BASE_URL не установлена.")

    web_browser.get(url)  # Используем url, загруженное из переменных окружения

    # Добавляем ожидание элемента с ID 'card-title'
    wait = WebDriverWait(web_browser, 10)
    element = wait.until(EC.presence_of_element_located((By.ID, "card-title")))

    # Проверяем, что текст элемента содержит "Авторизация"
    assert "Авторизация" in element.text  # Используем `element.text` для получения текста