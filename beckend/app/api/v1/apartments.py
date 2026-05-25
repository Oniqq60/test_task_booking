# app/api/v1/apartments.py
import logging
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.models.apartment import Apartment
from app.schemas.apartment import ApartmentRead, ApartmentCreate
from app.services.apartment import ApartmentService

router = APIRouter()
logger = logging.getLogger("app.api.apartments")


@router.get("", response_model=List[ApartmentRead])
def get_apartments(db: Session = Depends(get_db)):
    """Получить список всех квартир."""
    service = ApartmentService(db)
    return service.get_all()


@router.get("/{apartment_id}", response_model=ApartmentRead)
def get_apartment(apartment_id: uuid.UUID, db: Session = Depends(get_db)):
    """Получить квартиру по ID."""
    stmt = select(Apartment).where(Apartment.id == apartment_id)
    apartment = db.scalar(stmt)
    if not apartment:
        raise HTTPException(status_code=404, detail="Apartment not found")
    return ApartmentRead.model_validate(apartment)


@router.post("", response_model=ApartmentRead, status_code=status.HTTP_201_CREATED)
def create_apartment(
    title: str = Form(..., min_length=1, max_length=200),
    address: str = Form(..., min_length=1, max_length=500),
    price_per_day: float = Form(..., gt=0),
    owner_phone: str = Form(..., pattern=r"^\+7\d{10}$"),
    files: List[UploadFile] = File(default=[]),
    db: Session = Depends(get_db)
):
    service = ApartmentService(db)
    try:
        return service.create(
            title=title,
            address=address,
            price=price_per_day,
            phone=owner_phone,
            files=files
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating apartment: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{apartment_id}/booked-periods", response_model=List[dict])
def get_booked_periods(apartment_id: uuid.UUID, db: Session = Depends(get_db)):
    """Получить занятые периоды для квартиры."""
    service = ApartmentService(db)
    return [p.model_dump() for p in service.get_booked_periods(str(apartment_id))]