# Практика 2026 — Курс по backend-разработке

## Этап 1: Подготовка и основы

### Мини-проект: обработчик логов

Скрипт генерирует тестовые логи и парсит их двумя способами:
- `log_parser_slow.py` — неоптимизированная версия (O(n²))
- `log_parser_fast.py` — оптимизированная версия с использованием `Counter` и `defaultdict` (O(n))

### Как запустить

\`\`\`bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

python log_generator.py
python log_parser_slow.py
python log_parser_fast.py
\`\`\`

### Результаты сравнения производительности

| Версия | Кол-во строк | Время выполнения |
|--------|--------------|------------------|
| slow   | 50000        | 111.33 сек       |
| fast   | 50000        | 0.0360 сек       |

## Этап 2: CRUD API для заметок (Flask)

### Установка и запуск

\`\`\`bash
pip install -r requirements.txt
python run.py
\`\`\`

Сервер запустится на http://127.0.0.1:5000

### Эндпоинты API

| Метод | URL | Описание |
|-------|-----|----------|
| POST | /notes | Создать заметку |
| GET | /notes | Получить все заметки |
| GET | /notes/<id> | Получить заметку по id |
| PUT | /notes/<id> | Обновить заметку |
| DELETE | /notes/<id> | Удалить заметку |

### Пример запроса (curl)

\`\`\`bash
curl -X POST http://127.0.0.1:5000/notes \\
  -H "Content-Type: application/json" \\
  -d '{"title": "Тест", "content": "Пример заметки"}'
\`\`\`


## Этап 3: PostgreSQL, JOIN, фильтрация и пагинация

### Запуск PostgreSQL через Docker

\`\`\`bash
docker run --name notes-postgres -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=notes_db -p 5432:5432 -d postgres
\`\`\`

### Новые эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| POST | /categories | Создать категорию |
| GET | /categories | Получить все категории |
| GET | /notes?page=1&limit=10 | Список заметок с пагинацией |
| GET | /notes?category=Работа | Фильтрация заметок по категории |

### Пример запроса

\`\`\`bash
curl "http://127.0.0.1:5000/notes?category=Работа&page=1&limit=5"
\`\`\`

### Пример ответа

\`\`\`json
{
  "total": 3,
  "page": 1,
  "pages": 1,
  "notes": [
    {"id": 1, "title": "Встреча", "category": "Работа"}
  ]
}
\`\`\`


# Notes API

REST API для управления заметками с категориями, фильтрацией и пагинацией.

## Стек технологий

- Python 3.11
- Flask + Flask-SQLAlchemy
- PostgreSQL
- Docker / docker-compose
- pytest

## Функциональность

- CRUD операции с заметками
- Категории заметок
- Фильтрация по категории
- Пагинация результатов

## Локальный запуск

### Через Docker Compose (рекомендуется)

\`\`\`bash
git clone https://github.com/ayamoss/Project_note_manager_api.git
cd Project_note_manager_api
docker-compose up --build
\`\`\`

Приложение будет доступно на http://localhost:5000

### Без Docker

\`\`\`bash
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt

# Запустите PostgreSQL локально или через Docker
docker run --name notes-postgres -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=notes_db -p 5432:5432 -d postgres

python run.py
\`\`\`

## Тестирование

\`\`\`bash
pytest -v
\`\`\`

## API Эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| POST | /notes | Создать заметку |
| GET | /notes | Список заметок (пагинация, фильтр) |
| GET | /notes/<id> | Получить заметку |
| PUT | /notes/<id> | Обновить заметку |
| DELETE | /notes/<id> | Удалить заметку |
| POST | /categories | Создать категорию |
| GET | /categories | Список категорий |

## Примеры запросов

### Создать заметку

\`\`\`bash
curl -X POST http://localhost:5000/notes \\
  -H "Content-Type: application/json" \\
  -d '{"title": "Моя заметка", "content": "Текст", "category_id": 1}'
\`\`\`

### Получить заметки с фильтрацией и пагинацией

\`\`\`bash
curl "http://localhost:5000/notes?category=Работа&page=1&limit=5"
\`\`\`

### Создать категорию

\`\`\`bash
curl -X POST http://localhost:5000/categories \\
  -H "Content-Type: application/json" \\
  -d '{"name": "Работа"}'
\`\`\`

## Демо

Ссылка на задеплоенный сервис: https://notes-api.onrender.com

## Структура проекта

\`\`\`
.
├── app/
│   ├── __init__.py
│   ├── models.py
│   └── routes.py
├── tests/
│   ├── conftest.py
│   └── test_notes.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run.py
└── README.md
\`\`\`