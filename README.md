# Telegram Bot для поиска информации в Google Sheets

Этот бот для Telegram позволяет искать ФИО в Google Sheets и возвращает соответствующие значения.

## Настройка и Запуск

1. **Клонирование репозитория:**

```sh
git clone https://github.com/tonytkachenko/aiogram-gsheets.git
cd aiogram-gsheets
```

2. **Создание и активация виртуального окружения:**

```sh
python -m venv venv

source venv/bin/activate # Для Unix-подобных систем
.\venv\Scripts\activate # Для Windows
```

3. **Установка зависимостей:**

```sh
pip install -r requirements.txt
```

4. **Настройка переменных окружения:**

Переименуйте файл `.env.example` в `.env` в корневой директории проекта и введите свои значения для переменных

5. **Запуск бота:**

```sh

python bot.py
```

## Использование

Отправьте боту ФИО, и он найдет соответствующие записи в Google Sheets, возвращая номер п/п и итоговое значение.
