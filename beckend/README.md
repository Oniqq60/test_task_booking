# Apartments API 🏠

Backend для тестового задания: посуточная аренда квартир.

## 🚀 Быстрый старт

```bash
# 1. Клон и установка
git clone <repo>
cd backend
poetry install

# 2. Запуск БД
docker-compose up -d db

# 3. Миграции + сид
poetry run alembic upgrade head
poetry run python scripts/seed.py

# 4. Запуск сервера
poetry run uvicorn app.main:app --reload

# Docs: http://localhost:8000/docs