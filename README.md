##Тестовый пример SaaS проекта
Этот проект является тестовым примером SaaS приложения. 
Он предназначен для демонстрации основного шаблона архитектуры и принципов взаимодействия в рамках подобных проектов.

## Структура проекта

Проект включает в себя следующие основные компоненты:

```
├── requirements.txt         # Зависимости проекта
├── app/                     # Основная директория приложения
│   ├── __init__.py
│   ├── api/                 # API приложения
│   │   ├── main.py          # Основной модуль API
│   │   ├── __init__.py
│   │   ├── auth/            # Модули аутентификации
│   │   │   ├── auth_utils.py
│   │   │   ├── __init__.py
│   │   ├── handlers/        # Обработчики запросов
│   │   │   ├── docs.py
│   │   │   ├── webhooks.py
│   │   │   ├── __init__.py
│   │   ├── models/          # Модели данных
│   │   │   ├── standard.py
│   │   │   ├── webhooks.py
│   │   │   ├── __init__.py
│   │   ├── processing/      # Обработка данных
│   │       ├── parametr_sql_validator.py
│   │       ├── webhooks.py
│   │       ├── __init__.py
├── configs/                 # Конфигурации
│   ├── config.ini
│   ├── config.py
│   ├── __init__.py
├── database/                # Взаимодействие с базой данных
    ├── onlihub_objects.py
    ├── psql.py
    ├── __init__.py
```

Извините за недоразумение. Вот более подробная инструкция для включения в ваш `README.md`:

---

## Установка и запуск

Чтобы запустить проект, выполните следующие шаги:

1. Клонируйте репозиторий:
   ```
   git clone https://github.com/Vangardo/test_saas
   ```

2. Перейдите в директорию проекта:
   ```
   cd test_saas
   ```

3. Установите необходимые зависимости:
   ```
   pip install -r requirements.txt
   ```

4. Перейдите в папку `app`, где находится файл `main.py`:
   ```
   cd app
   ```

5. Запустите приложение с помощью Uvicorn:
   ```
   uvicorn main:app --port 8016
   ```

Это запустит сервер на порту 8016. Теперь вы можете обращаться к вашему приложению через указанный порт.


---

## Задание

Цель задания - расширение функциональности проекта за счет добавления нового эндпоинта для управления складами. Реализация нового эндпоинта должна быть выполнена в соответствии с существующей архитектурой проекта и структурой, используемой для вебхуков.

### Описание эндпоинта Warehouses

Создайте эндпоинт `Warehouses`, который будет включать в себя следующие операции:

- **Создание склада:** Добавление нового склада в базу данных.
- **Обновление склада:** Изменение информации о существующем складе.
- **Удаление склада:** Удаление склада из базы данных.
- **Получение информации о конкретном складе:** Вывод данных одного выбранного склада.
- **Получение списка всех складов:** Вывод списка всех складов с информацией о них.

Проверка безопасности должна быть реализована аналогично тому, как это сделано в эндпоинтах вебхуков.

### Структура таблицы Warehouses в базе данных

Таблица `Warehouses` в базе данных должна содержать следующие колонки:

- `id`: Уникальный идентификатор склада.
- `title`: Название склада.
- `user_id`: Идентификатор пользователя, ответственного за склад.
- `integration_id`: Идентификатор интеграции.
- `status_id`: Идентификатор статуса склада.

### Связи с другими таблицами

При получении информации о складах необходимо учитывать связи с другими таблицами:

- **Соединение с таблицей `integrations` по колонке `integration_id`**: При выводе информации о складе или списка складов следует включать `title` из таблицы `integrations`.
- **Соединение с таблицей `Warehouse_statuses` по колонке `status_id`**: Аналогично, включать информацию о статусе склада, получая `title` из таблицы `Warehouse_statuses`.



