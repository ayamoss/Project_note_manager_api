# Notes API — сервис управления заметками

REST API для заметок с категориями, фильтрацией и пагинацией.

**Демо:** https://av-project.onrender.com

---

## Стек

- Python 3.11
- Flask + Flask-SQLAlchemy + Flask-Migrate
- PostgreSQL (продакшн) / SQLite (локально)
- Docker + docker-compose
- gunicorn (WSGI-сервер)
- pytest (тесты)
- Render (хостинг)

---

## Структура проекта

```
.
├── app/
│   ├── __init__.py      # фабрика create_app()
│   ├── models.py        # модели Note и Category
│   └── routes.py        # REST API эндпоинты
├── migrations/          # Alembic-миграции
├── scripts/             # скрипты из модуля 1 (логи)
│   ├── log_generator.py
│   ├── log_parser_slow.py   # O(n²)
│   └── log_parser_fast.py   # O(n)
├── tests/
│   ├── conftest.py
│   └── test_notes.py    # 11 тестов
├── Dockerfile
├── entrypoint.sh        # миграции при старте
├── docker-compose.yml
├── requirements.txt
├── run.py
└── README.md
```

---

## Быстрый старт

### Локально

```bash
git clone https://github.com/ayamoss/Project_note_manager_api.git
cd Project_note_manager_api

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate      # Linux/macOS

pip install -r requirements.txt

cp .env.example .env           # заполнить DATABASE_URL и SECRET_KEY

flask db upgrade               # применить миграции
python run.py
```

Сервис: http://127.0.0.1:5000

### Через Docker

```bash
docker-compose up --build
```

Поднимутся `web` (Flask + gunicorn) и `db` (PostgreSQL 15).

---

## Переменные окружения

| Переменная | Описание |
|------------|----------|
| `DATABASE_URL` | Строка подключения к БД |
| `SECRET_KEY` | Секретный ключ Flask |

Скопируй `.env.example` → `.env`. **Файл `.env` не коммитится.**

---

## API

### Категории

| Метод | URL | Описание |
|-------|-----|----------|
| `POST` | `/categories` | Создать категорию |
| `GET` | `/categories` | Список категорий |

### Заметки

| Метод | URL | Описание |
|-------|-----|----------|
| `POST` | `/notes` | Создать заметку |
| `GET` | `/notes` | Список (пагинация + фильтр) |
| `GET` | `/notes/<id>` | Получить заметку |
| `PUT` | `/notes/<id>` | Обновить заметку |
| `DELETE` | `/notes/<id>` | Удалить заметку |

**Query-параметры `GET /notes`:** `page`, `limit`, `category`.

---

## Примеры запросов

### Создать категорию

```bash
curl -X POST https://av-project.onrender.com/categories \
  -H "Content-Type: application/json" \
  -d '{"name": "Учеба"}'
```

### Создать заметку

```bash
curl -X POST https://av-project.onrender.com/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "СВФУ, ИМИ", "content": "Б-ММИМИ-24", "category_id": 1}'
```

### Получить все заметки

```bash
curl https://av-project.onrender.com/notes
```

### Фильтр + пагинация

```bash
curl "https://av-project.onrender.com/notes?category=Учеба&page=1&limit=5"
```

### Обновить

```bash
curl -X PUT https://av-project.onrender.com/notes/2 \
  -H "Content-Type: application/json" \
  -d '{"title": "Новый заголовок"}'
```

### Удалить

```bash
curl -X DELETE https://av-project.onrender.com/notes/2
```

---

## Коды ответов

| Код | Когда |
|-----|-------|
| `200` | GET / PUT |
| `201` | POST |
| `204` | DELETE |
| `400` | Невалидные данные |
| `404` | Объект не найден |

---

## Тесты

```bash
pytest -v
```

11 тестов: CRUD, валидация, категории, фильтрация, пагинация.
Используется SQLite in-memory с `StaticPool`.

---

## Миграции

```bash
flask db migrate -m "описание"   # создать
flask db upgrade                 # применить
flask db downgrade               # откатить
```

На Render миграции применяются **автоматически** через `entrypoint.sh`.

---

## Модуль 1 — обработчик логов

| Скрипт | Сложность | Время (50 000 строк) |
|--------|-----------|----------------------|
| `log_parser_slow.py` | O(n²) | ~111 сек |
| `log_parser_fast.py` | O(n) | ~0.036 сек |

```bash
cd scripts
python log_generator.py
python log_parser_slow.py
python log_parser_fast.py
```

---

## Деплой на Render

- **PostgreSQL** — создан на Render.
- **Web Service** — собирается из `Dockerfile` (Runtime: Docker).
- **Миграции** — `entrypoint.sh` выполняет `flask db upgrade` перед запуском.
- **Переменные** — `DATABASE_URL`, `SECRET_KEY` заданы в панели Render.

---

## Демо

🔗 **https://av-project.onrender.com**

> Free-план Render: после 15 минут простоя сервис «засыпает». Первый запрос может занять до 50 секунд.

---

## Автор

**Аммосова Виктория** — [@ayamoss](https://github.com/ayamoss)

Практика 2026