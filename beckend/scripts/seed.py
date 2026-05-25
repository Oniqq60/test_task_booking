#!/usr/bin/env python3
"""Seed demo apartments with photos from local img folder"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import create_engine, delete
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.apartment import Apartment
from app.models.booking import Booking
from app.models.photo import ApartmentPhoto
from app.models.base import Base


def seed():
    engine = create_engine(str(settings.sync_database_url))
    Base.metadata.create_all(engine)
    
    with Session(engine) as db:
        db.execute(delete(Booking))
        db.execute(delete(ApartmentPhoto))
        db.execute(delete(Apartment))
        db.commit()
        print("🗑️ Старые записи удалены")

        apartments = [
            Apartment(
                title="Уютная двушка у метро",
                address="Москва, ул. Примерная, 12",
                price_per_day=4500.00,
                owner_phone="+79991234567"
            ),
            Apartment(
                title="Студия в центре",
                address="Москва, Тверская, 45",
                price_per_day=3200.00,
                owner_phone="+79997654321"
            ),
            Apartment(
                title="Лофт с панорамными окнами",
                address="Москва, Сити, Башня Федерация",
                price_per_day=8900.00,
                owner_phone="+79991112233"
            ),
        ]
        
        db.add_all(apartments)
        db.flush()
        
        img_dir = Path(__file__).resolve().parent.parent / "img"
        supported_exts = {".jpg", ".jpeg", ".png", ".webp"}
        image_files = sorted([
            f for f in img_dir.iterdir() 
            if f.is_file() and f.suffix.lower() in supported_exts
        ])
        
        content_type_map = {
            ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".png": "image/png", ".webp": "image/webp"
        }
        
        photos_to_add = []
        for i, apt in enumerate(apartments):
            if i < len(image_files):
                img_path = image_files[i]
                try:
                    with open(img_path, "rb") as f:
                        photos_to_add.append(ApartmentPhoto(
                            apartment_id=apt.id,
                            content_type=content_type_map.get(img_path.suffix.lower(), "image/jpeg"),
                            data=f.read()
                        ))
                    print(f"✅ Добавлено фото {img_path.name} для квартиры '{apt.title}'")
                except Exception as e:
                    print(f"⚠️ Ошибка чтения {img_path.name}: {e}")
        
        if photos_to_add:
            db.add_all(photos_to_add)
            db.commit()
            print(f"✅ Добавлено {len(apartments)} квартир и {len(photos_to_add)} фото")


if __name__ == "__main__":
    seed()