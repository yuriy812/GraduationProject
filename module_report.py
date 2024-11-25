# module_report.py
import os
import pandas as pd
from datetime import datetime

# Глобальный список для хранения результатов тестов
results = []


def save_results(results):
    if not results:
        print("Нет результатов для сохранения.")
        return

        # Создание DataFrame из результатов
    # Добавление больше информации о тестах  
    df = pd.DataFrame(results)

    # Переименование столбцов для большей ясности  
    df.rename(columns={
        'test': 'Название теста',
        'status': 'Статус',
        'error': 'Ошибка',
        'timestamp': 'Время'
    }, inplace=True)

    report_dir = 'reports'

    # Создание директории, если она не существует
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
        print(f"Создана директория: {report_dir}")

    excel_path = os.path.join(report_dir, 'test_report.xlsx')

    # Если файл уже существует, он будет перезаписан
    try:
        # Запись данных в файл Excel
        df.to_excel(excel_path, index=False)
        print(f"Отчет успешно сохранен в {excel_path}")
    except Exception as e:
        print(f"Ошибка при сохранении отчета: {e}")

    # Функция может быть вызвана для сохранения результатов тестов

# Пример использования
if __name__ == "__main__":
    # Здесь можно добавить тестовые данные для проверки
    sample_results = [
        {'test': 'Login Test', 'status': 'Passed', 'timestamp': datetime.now()},
        {'test': 'Login Test', 'status': 'Passed', 'timestamp': datetime.now()}
    ]
    save_results(sample_results)
