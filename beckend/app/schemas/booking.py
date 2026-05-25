from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import date
from uuid import UUID
import re

class BookingCreate(BaseModel):
    apartment_id: UUID
    guest_name: str = Field(..., min_length=2, max_length=100)
    guest_phone: str
    check_in: date
    check_out: date
    
    @field_validator("guest_phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        patterns = [r"^\+7\d{10}$", r"^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$"]
        if not any(re.match(p, v) for p in patterns):
            raise ValueError("Phone must be in E.164 or +7 (XXX) XXX-XX-XX format")
        return v
    
    @field_validator("check_out")
    @classmethod
    def validate_dates(cls, check_out: date, info) -> date:
        check_in = info.data.get("check_in")
        if check_in and check_out <= check_in:
            raise ValueError("check_out must be after check_in")
        if check_out < date.today():
            raise ValueError("Dates cannot be in the past")
        return check_out
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "apartment_id": "550e8400-e29b-41d4-a716-446655440000",
            "guest_name": "Артём",
            "guest_phone": "+79990000000",
            "check_in": "2026-06-10",
            "check_out": "2026-06-15"
        }
    })

class BookingRead(BaseModel):
    id: UUID
    apartment_id: UUID
    guest_name: str
    guest_phone: str
    check_in: date
    check_out: date
    model_config = ConfigDict(from_attributes=True)

class BookedPeriod(BaseModel):
    check_in: date
    check_out: date
    model_config = ConfigDict(from_attributes=True)