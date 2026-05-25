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

```bash
GET http://localhost:8000/api/v1/apartments
POST http://localhost:8000/api/v1/apartments
title - Text - Тестовая квартира
address - Text - г. Москва, ул. Тестовая, 1
price_per_day - Text - 5000
owner_phone - Text - +79991234567
files - File - .jpg/.png

GET http://localhost:8000/api/v1/apartments/{{apartment_id}}
GET http://localhost:8000/api/v1/apartments/{{apartment_id}}/booked-periods
```

```bash
POST http://localhost:8000/api/v1/bookings
{
  "apartment_id": "{{apartment_id}}",
  "guest_name": "Артём Иванов",
  "guest_phone": "+79991112233",
  "check_in": "2026-06-10",
  "check_out": "2026-06-15"
}

GET http://localhost:8000/api/v1/bookings
GET http://localhost:8000/api/v1/bookings/{{booking_id}}
```

```bash
GET http://localhost:8000/api/v1/photos/{{photo_id}}
```
