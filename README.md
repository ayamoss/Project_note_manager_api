# Notes API — сервис управления заметками

REST API для управления заметками с категориями, фильтрацией и пагинацией.

**Демо:** https://av-project.onrender.com

---

## Стек технологий

- **Python 3.11**
- **Flask 3.1** + **Flask-SQLAlchemy 3.1**
- **Flask-Migrate** (Alembic) — миграции БД
- **PostgreSQL 18** (продакшн) / SQLite (локально)
- **Docker** + **docker-compose**
- **gunicorn** — WSGI-сервер для продакшна
- **pytest** — тестирование
- **Render** — хостинг

---

## Структура проекта

```
.
├── app/
│   ├── __init__.py         # фабрика приложения create_app()
│   ├── models.py           # модели Note и Category
│   └── routes.py           # REST API эндпоинты
├── migrations/             # Alembic-миграции
│   ├── versions/
│   │   └── 330acf37c686_initial_tables.py
│   ├── alembic.ini
│   └── env.py
├── scripts/                # скрипты из модуля 1
│   ├── log_generator.py    # генератор тестовых логов
│   ├── log_parser_slow.py  # медленный парсер (O(n²))
│   └── log_parser_fast.py  # оптимизированный (O(n))
├── tests/
│   ├── conftest.py         # фикстуры pytest
│   └── test_notes.py       # 11 тестов
├── Dockerfile
├── entrypoint.sh           # применение миграций при старте
├── docker-compose.yml
├── requirements.txt
├── run.py                  # точка входа
└── README.md
```

---

## Быстрый старт

### Локально без Docker

```bash
# 1. Клонировать репозиторий
git clone https://github.com/ayamoss/Project_note_manager_api.git
cd Project_note_manager_api

# 2. Виртуальное окружение
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate      # Linux/macOS

# 3. Зависимости
pip install -r requirements.txt

# 4. Переменные окружения — скопировать .env.example в .env и заполнить
cp .env.example .env

# 5. Применить миграции
flask db upgrade

# 6. Запустить
python run.py
```

Сервис будет доступен на `http://127.0.0.1:5000`.

### Через Docker Compose

```bash
docker-compose up --build
```

Поднимутся два контейнера: `web` (Flask + gunicorn) и `db` (PostgreSQL 15).
Сервис — на `http://localhost:5000`.

---

## Переменные окружения

| Переменная | Описание | Пример |
|------------|----------|--------|
| `DATABASE_URL` | Строка подключения к БД | `postgresql://postgres:pass@localhost:5432/notes_db` |
| `SECRET_KEY` | Секретный ключ Flask | `change-me-in-production` |

Скопируй `.env.example` → `.env` и заполни своими значениями.
**Файл `.env` не коммитится в Git.**

---

## API эндпоинты

### Категории

| Метод | URL | Описание |
|-------|-----|----------|
| `POST` | `/categories` | Создать категорию |
| `GET` | `/categories` | Список категорий |

### Заметки

| Метод | URL | Описание |
|-------|-----|----------|
| `POST` | `/notes` | Создать заметку |
| `GET` | `/notes` | Список заметок (пагинация + фильтрация) |
| `GET` | `/notes/<id>` | Получить заметку по id |
| `PUT` | `/notes/<id>` | Обновить заметку |
| `DELETE` | `/notes/<id>` | Удалить заметку |

### Query-параметры для `GET /notes`

| Параметр | Тип | По умолчанию | Описание |
|----------|-----|--------------|----------|
| `page` | int | `1` | Номер страницы |
| `limit` | int | `10` | Заметок на странице |
| `category` | string | — | Фильтр по имени категории |

---

## Примеры запросов (curl)

### Создать категорию

```bash
curl -X POST https://av-project.onrender.com/categories \
  -H "Content-Type: application/json" \
  -d '{"name": "Учеба"}'
```

**Ответ `201 Created`:**
```json
{"id": 1, "name": "Учеба"}
```

### Создать заметку

```bash
curl -X POST https://av-project.onrender.com/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "СВФУ, ИМИ", "content": "Б-ММИМИ-24", "category_id": 1}'
```

**Ответ `201 Created`:**
```json
{
  "id": 2,
  "title": "СВФУ, ИМИ",
  "content": "Б-ММИМИ-24",
  "created_at": "2026-09-22T15:42:02.618912",
  "category": "Учеба"
}
```

### Получить все заметки

```bash
curl https://av-project.onrender.com/notes
```

**Ответ `200 OK`:**
```json
{
  "total": 2,
  "page": 1,
  "pages": 1,
  "notes": [
    {"id": 2, "title": "СВФУ, ИМИ", "category": "Учеба"},
    {"id": 1, "title": "Первая заметка", "category": null}
  ]
}
```

### Фильтрация и пагинация

```bash
curl "https://av-project.onrender.com/notes?category=Учеба&page=1&limit=5"
```

### Получить одну заметку

```bash
curl https://av-project.onrender.com/notes/2
```

### Обновить заметку

```bash
curl -X PUT https://av-project.onrender.com/notes/2 \
  -H "Content-Type: application/json" \
  -d '{"title": "Обновлённый заголовок"}'
```

### Удалить заметку

```bash
curl -X DELETE https://av-project.onrender.com/notes/2
```

**Ответ:** `204 No Content`.

### Получить категории

```bash
curl https://av-project.onrender.com/categories
```

---

## Коды ответов

| Код | Когда возвращается |
|-----|---------------------|
| `200 OK` | Успешный GET / PUT |
| `201 Created` | Успешный POST |
| `204 No Content` | Успешный DELETE |
| `400 Bad Request` | Невалидные данные (нет `title`, дубликат категории, несуществующий `category_id`) |
| `404 Not Found` | Заметка с таким id не найдена |

---

## Тестирование

```bash
pytest -v
```

**Покрытие:** 11 тестов

- CRUD заметок (create, read, update, delete)
- Валидация (отсутствие обязательного поля, несуществующий id)
- Создание категорий
- Фильтрация по категории
- Пагинация

Все тесты используют SQLite in-memory с `StaticPool` — изолированно от продакшн-БД.

---

## Миграции

```bash
# Создать новую миграцию
flask db migrate -m "описание изменений"

# Применить миграции
flask db upgrade

# Откатить последнюю
flask db downgrade
```

При деплое миграции применяются **автоматически** — `entrypoint.sh` выполняет `flask db upgrade` перед запуском gunicorn.

---

## Модуль 1 — обработчик логов

Скрипты в `scripts/` демонстрируют оптимизацию алгоритма:

| Скрипт | Сложность | Время на 50 000 строк |
|--------|-----------|------------------------|
| `log_parser_slow.py` | O(n²) | ~111 сек |
| `log_parser_fast.py` | O(n) | ~0.036 сек |

**Запуск:**

```bash
cd scripts
python log_generator.py       # сгенерировать app.log
python log_parser_slow.py     # медленная версия
python log_parser_fast.py     # быстрая версия
```

---

## Деплой на Render

Сервис задеплоен через **Docker** на Render:

1. **PostgreSQL** — создан в Render (Singapore).
2. **Web Service** — собирается из `Dockerfile`.
3. **Миграции** — применяются в `entrypoint.sh` при старте контейнера.
4. **Переменные окружения** — `DATABASE_URL`, `SECRET_KEY` заданы в панели Render.

**Команда запуска (Dockerfile):**

```dockerfile
CMD ["/app/entrypoint.sh"]
```

**entrypoint.sh:**

```sh
#!/bin/sh
set -e
flask db upgrade
exec gunicorn -b 0.0.0.0:$PORT run:app
```

---

## Демо

🔗 **https://av-project.onrender.com**

**Проверка:**

```bash
curl https://av-project.onrender.com/notes
```

> ⚠️ Сервис на **Free-плане Render** — после 15 минут простоя «засыпает». Первый запрос может занять до 50 секунд. Второй — мгновенный.

---

## Автор

**Аммосова Виктория** — [@ayamoss](https://github.com/ayamoss)

Практика 2026