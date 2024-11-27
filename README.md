

# GraduationProject
### Необходимо протестировать новый интерфейс авторизации в личном кабинете от заказчика Ростелеком.

- Объект тестирования: https://b2c.passport.rt.ru

- [Требования по проекту (.doc)](https://docs.google.com/document/d/12yoTwHSTXxIUQQCH32OvlSd3QYUt_aQk/edit?usp=sharing&ouid=114302123057644378289&rtpof=true&sd=true)

## Описание проекта  

GraduationProject — это набор автоматизированных тестов для проверки функциональности формы авторизации и регистрации веб-приложения "Ростелеком".   Проект включает тесты для авторизации и регистрации пользователей с использованием различных методов, таких как электронная почта, логин и телефон, а также обработку капчи.  
- [Тест-кейсы, дефекты (.excel, pdf)](https://drive.google.com/drive/folders/1VG3AksJ-4hhcnIDxIjWWwzjIB6_4Fcjg?usp=sharing)
## Структура проекта  

```
    GraduationProject
    │
    ├── __init__.py
    ├── locators.py
    ├── module_report.py
    ├── module_screenshot.py
    ├── reports/
    ├── settings.py
    └── tests/
        ├── images/
        ├── __init__.py
        ├── conftest.py
        ├── authorization.py
        ├── test_data.json
        ├── negative_authorization.py
        └── registration.py
```

### Описание файлов  

- `__init__.py`: Инициализация пакета.  
- `locators.py`: Определение локаторов элементов на веб-странице для использования в тестах.  
- `module_report.py`: Модуль для генерации отчетов о результатах тестирования.  
- `module_screenshot.py`: Модуль для создания скриншотов при возникновении ошибок.  
- `reports/`: Директория для хранения отчетов о тестировании.  
- `settings.py`: Настройки проекта, включая URL веб-приложения.  
- `tests/`: Директория с тестами.  
  - `images/`: Директория для хранения изображений, таких как капчи.  
  - `conftest.py`: Конфигурация для pytest, включая фикстуры.  
  - `authorization.py`: Тесты для проверки авторизации пользователей.  
  - `test_data.json`: Файл с тестовыми данными для авторизации.  
  - `negative_authorization.py`: Тесты для проверки неудачной авторизации.  
  - `registration.py`: Тесты для проверки регистрации пользователей.  

## Тестовые сценарии  

Проект включает следующие тестовые сценарии:  

- **Тесты авторизации**:  
  - Проверка успешной авторизации через email.  
  - Проверка успешной авторизации через логин.  
  - Проверка некорректных данных регистрации через email.  
  - Проверка некорректных данных регистрации через телефон.  
  - Обработка капчи при авторизации.  
  - Проверка неудачной авторизации (некорректные данные).
  - Проверка по коду восстановления пароля.
  
Применялась *доменное тестирование* — это техника тестирования метода чёрного ящика, направленная на уменьшение количества   тестов путём одновременной проверки множества различных позитивных значений. Данная техника базируется на одновременном использовании техник эквивалентного разбиения и анализа граничных значений.

*Цель доменного тестирования* — предоставить стратегию по выбору минимального набора показательных тестов.
Доменное тестирование позволяет тестировать нескольких переменных одновременно. Существуют две причины, по которым стоит обратить на это внимание:

Редко будет достаточно времени на создание тест-кейсов для каждой переменной в системе.
Шаги для достижения цели:
1. Для начала нужно разделить предполагаемые значения на отдельные группы, условия - это могут быть:
    разные значения, диапазон значений

    разные форматы файлов: допустимые форматы, недопустимые форматы 

    разное количество символов: допустимое количество(минимальное, среднее, максимальное), меньше минимального, пустое значение, больше максимального.

    уникальность: уникальный, неуникальны

    разный регистр: алфавитные в смешанном регистре, в нижнем регистре, в верхнем регистре

    разные символы: цифровые, алфавитные, разные языки, спецсимволы, разные кодировки

    наличие пробелов: в начале, в середине, в конце

2. Выявить конкретный набор значений и выбрать из них наиболее показательные, представляющие каждую группу, включая обязательно границы. 
3. Скомбинировать эти значения (позитивные тесты) таким образом, чтобы отдельные параметры можно было протестировать одновременно.
 
###  Принципы:

Производить сразу несколько позитивных тестов (например, ввод данных в несколько полей), вместо одного
    предполагаемые граничные значения. Во избежание эффекта пестицида, при повторе тестов использовать разные эквивалентные значения.
В случае, если использование спецсимволов ведёт к ошибке, то рекомендуется каждый спецсимвол проверять отдельно.

*Исследовательское тестирование* — это форма тестирования, которая проводится без плана. В таком виде тестирования просто изучаем приложение.



## Установка  

Для запуска тестов убедитесь, что у вас установлен Python 3 и pip. Затем выполните следующие команды:  

1. Клонируйте репозиторий:  

   ```bash  
   git clone https://github.com/ваш_пользователь/GraduationProject.git  
   cd GraduationProject
   ```

2. Установите необходимые зависимости:  

   ```bash  
   pip install -r requirements.txt  
   ```  

   Если файла `requirements.txt` нет, установите необходимые пакеты вручную:  

   ```bash  
   pip install pytest selenium requests easyocr  

### При разработке тест-кейсов были применены следующие техники тест-дизайна: 
 
* эквивалентное разбиение
* ```  
### Инструменты, которые применялись для тестирования.

* Для тестирования сайта был использован 
инструмент [Selenium](https://www.selenium.dev/);
* Для определения локаторов использовались 
следующие инструменты: DevTools, [ChroPath](https://chrome.google.com/webstore/detail/chropath/ljngjbnaijcbncmcnjfhigebomdlkcjo). 
* Платформы для управления тестированием `qase.io`
## Запуск тестов  

Для запуска тестов используйте следующую команду:

```bash
pytest tests/
```  

Эта команда выполнит все тесты в директории `tests/` и выведет результаты в консоль.

## Лицензия  

Этот проект лицензирован под MIT License.


