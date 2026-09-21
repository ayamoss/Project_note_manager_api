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