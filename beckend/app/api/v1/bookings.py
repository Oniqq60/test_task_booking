import logging
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingRead
from app.services.booking import BookingService

router = APIRouter()
logger = logging.getLogger("app.api.bookings")


@router.post("", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
def create_booking(booking_in: BookingCreate, db: Session = Depends(get_db)):
    """Создать новое бронирование."""
    service = BookingService(db)
    return service.create(booking_in)


@router.get("", response_model=List[BookingRead])
def get_bookings(db: Session = Depends(get_db)):
    """Получить список всех бронирований."""
    stmt = select(Booking)
    bookings = db.scalars(stmt).all()
    return [BookingRead.model_validate(b) for b in bookings]


@router.get("/{booking_id}", response_model=BookingRead)
def get_booking(booking_id: uuid.UUID, db: Session = Depends(get_db)):
    """Получить бронирование по ID."""
    stmt = select(Booking).where(Booking.id == booking_id)
    booking = db.scalar(stmt)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return BookingRead.model_validate(booking)