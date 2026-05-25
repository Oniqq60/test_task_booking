import logging
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.booking import Booking
from app.schemas.booking import BookingCreate
from app.core.exceptions import ConflictError, ValidationError, NotFoundError

logger = logging.getLogger("app.services.booking")

class BookingService:
    def __init__(self, db: Session):
        self.db = db
        self.logger = logger

    def create(self, booking_in: BookingCreate) -> Booking:
        self.logger.debug(f"🔍 Валидация дат: {booking_in.check_in} -> {booking_in.check_out}")
        
        if booking_in.check_in >= booking_in.check_out:
            self.logger.warning("⚠️ Попытка создать бронь с check_in >= check_out")
            raise ValidationError("Дата выезда должна быть позже даты заезда")

        overlap = (
            self.db.query(Booking)
            .filter(
                Booking.apartment_id == booking_in.apartment_id,
                Booking.check_in < booking_in.check_out,
                Booking.check_out > booking_in.check_in
            )
            .first()
        )

        if overlap:
            self.logger.warning(
                f"⛔ Конфликт бронирования: Apartment {booking_in.apartment_id} "
                f"занят с {overlap.check_in} по {overlap.check_out}"
            )
            raise ConflictError("Выбранные даты уже забронированы")

        new_booking = Booking(**booking_in.model_dump())
        self.db.add(new_booking)
        self.db.commit()
        self.db.refresh(new_booking)
        
        self.logger.info(f"✅ Бронирование создано: ID {new_booking.id} | Apartment {booking_in.apartment_id}")
        return new_booking