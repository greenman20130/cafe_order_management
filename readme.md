# Cafe Order Management

## Описание

Cafe Order Management — это веб-приложение для управления заказами в кафе. Приложение позволяет добавлять, редактировать, удалять и просматривать заказы, а также генерировать отчеты о выручке.

## Функциональные возможности

- Добавление, редактирование и удаление заказов.
- Просмотр списка всех заказов.
- Фильтрация заказов по статусу и номеру стола.
- Генерация отчета о выручке.
- REST API для работы с заказами.

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/greenman20130/cafe_order_management.git
   cd cafe_order_management
   ```
2. Создайте и активируйте виртуальное окружение:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Linux/Mac
   venv\Scripts\activate  # Для Windows
   ```
3. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```
4. Примените миграции:

   ```bash
   python manage.py migrate
   ```
5. Запустите сервер:

   ```bash
   python manage.py runserver
   ```
6. Откройте браузер и перейдите по адресу `http://127.0.0.1:8000/orders`.

## API

API доступна по адресу `/orders/api`.
