# 0. Настройка переменных окружения:
cp beckend/.env.example beckend/.env
cp frontend/.env.example frontend/.env

# 1. Запуск всех сервисов
```bash
docker compose up -d
```

Команда поднимет:
db PostgreSQL на порту 5432
backend FastAPI на порту 8000
frontend Next.js на порту 3000

# 2. Применение миграций и сид-данных
```bash
# Применить миграции БД
docker compose exec backend poetry run alembic upgrade head

# Заполнить БД тестовыми данными (квартиры + фото)
docker compose exec backend poetry run python scripts/seed.py
```
# 3. Проверка готовности
```bash
docker compose ps  

curl http://localhost:8000/health
```

Frontend: http://localhost:3000
Backend API: http://localhost:8000
Swagger Docs: http://localhost:8000/docs