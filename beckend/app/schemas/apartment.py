# app/schemas/apartment.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
import uuid


class ApartmentBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    address: str = Field(..., min_length=1, max_length=500)
    price_per_day: float = Field(..., gt=0)
    owner_phone: str = Field(..., pattern=r"^\+7\d{10}$")


class ApartmentCreate(ApartmentBase):
    """Schema for creating an apartment (used in tests)."""
    pass


class ApartmentRead(ApartmentBase):
    id: uuid.UUID
    photos: List["PhotoRead"] = []
    
    class Config:
        from_attributes = True


class PhotoRead(BaseModel):
    id: uuid.UUID
    apartment_id: uuid.UUID
    content_type: str
    
    class Config:
        from_attributes = True


class BookedPeriod(BaseModel):
    check_in: date
    check_out: date

ApartmentRead.model_rebuild()