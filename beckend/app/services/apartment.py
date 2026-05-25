# app/services/apartment.py
import logging
from typing import List
from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.apartment import Apartment
from app.models.photo import ApartmentPhoto
from app.schemas.apartment import ApartmentRead, BookedPeriod
from app.core.exceptions import NotFoundError

logger = logging.getLogger("app.services.apartment")


class ApartmentService:
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    
    def __init__(self, db: Session):
        self.db = db
        self.logger = logger

    def get_all(self) -> List[ApartmentRead]:
        """Получить все квартиры с фото."""
        stmt = select(Apartment)
        apartments = self.db.scalars(stmt).all()
        return [ApartmentRead.model_validate(apt) for apt in apartments]

    def create(
        self,
        title: str,
        address: str,
        price: float,
        phone: str,
        files: List[UploadFile]
    ) -> ApartmentRead:
        """Создать квартиру с фотографиями."""
        for file in files:
            if file.size and file.size > self.MAX_FILE_SIZE:
                raise ValueError(f"File {file.filename} exceeds size limit (10MB)")
            
            ext = file.filename.split(".")[-1].lower()
            if f".{ext}" not in self.ALLOWED_EXTENSIONS:
                raise ValueError(f"File {file.filename} has invalid extension")
        
        apartment = Apartment(
            title=title,
            address=address,
            price_per_day=price,
            owner_phone=phone,
            photos=[]
        )
        
        self.db.add(apartment)
        self.db.flush()
        
        if files:
            photos = []
            for file in files:
                content = file.file.read()
                photo = ApartmentPhoto(
                    apartment_id=apartment.id,
                    content_type=file.content_type or "image/jpeg",
                    data=content
                )
                photos.append(photo)
            
            self.db.add_all(photos)
        
        self.db.commit()
        self.db.refresh(apartment)
        
        self.logger.info(f"✅ Квартира создана: ID {apartment.id} | {title}")
        return ApartmentRead.model_validate(apartment)

    def get_booked_periods(self, apartment_id: str) -> List[BookedPeriod]:
        """Получить занятые периоды для квартиры."""
        apt_stmt = select(Apartment).where(Apartment.id == apartment_id)
        if not self.db.scalar(apt_stmt):
            raise NotFoundError("Apartment not found")
        
        stmt = select(Booking).where(Booking.apartment_id == apartment_id)
        bookings = self.db.scalars(stmt).all()
        return [BookedPeriod(check_in=b.check_in, check_out=b.check_out) for b in bookings]