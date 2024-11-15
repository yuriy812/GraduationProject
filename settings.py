# settings.py
import os
from dotenv import load_dotenv

load_dotenv()

valid_email = os.getenv("USER_EMAIL")  # заключите имя переменной в кавычки
valid_password = os.getenv("USER_PASSWORD")  # заключите имя переменной в кавычки
url = os.getenv("BASE_URL")