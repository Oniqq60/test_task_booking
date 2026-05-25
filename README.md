1. Запуск всех сервисов
```bash
docker compose up -d
```

Команда поднимет:
db PostgreSQL на порту 5432
backend FastAPI на порту 8000
frontend Next.js на порту 3000

2. Применение миграций и сид-данных
```bash
# Применить миграции БД
docker compose exec backend alembic upgrade head

# Заполнить БД тестовыми данными (квартиры + фото)
docker compose exec backend python scripts/seed.py
```

Frontend: http://localhost:3000
Backend API: http://localhost:8000
Swagger Docs: http://localhost:8000/docs


# 2. Перезапустите миграции
docker-compose exec backend poetry run alembic upgrade head

# 3. Перезапустите backend
docker-compose restart backend

# 4. Проверьте
curl http://localhost:8000/api/v1/bookings