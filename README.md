# УЛП ИБ 2025

## Локальный запуск проекта

1.  Клонируйте репозиторий:
    ```bash
    git clone https://github.com/Jahamars/ibpp2025.git
    ```

2.  Создайте и активируйте виртуальное окружение:
    ```bash
    python -m venv ibpp2025
    
    # Для Windows
    ibpp2025\Scripts\activate
    
    # Для Linux
    source ibpp2025 /bin/activate
    ```

3.  Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

    
4.  Запустите PostgreSQL сервер , с базой и ползователем 

5.  Настройте переменные окружения:
    *   Откройте файл `.env` и впишите ваши данные для `SECRET_KEY` и подключения к базе данных PostgreSQL (`DB_NAME`, `DB_USER`, `DB_PASSWORD`).


6.  Примените миграции для создания таблиц в БД:
    ```bash
    python manage.py migrate
    ```

7.  Запустите сервер для разработки:
    ```bash
    python manage.py runserver
    ```
