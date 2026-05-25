from datetime import date
import uuid
from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, UUIDMixin, TimestampMixin

class Booking(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "bookings"
    
    apartment_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("apartments.id"), nullable=False, index=True)
    guest_name: Mapped[str] = mapped_column(String(100), nullable=False)
    guest_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    check_in: Mapped[date] = mapped_column(nullable=False, index=True)
    check_out: Mapped[date] = mapped_column(nullable=False, index=True)
    
    apartment = relationship("Apartment", back_populates="bookings")
    
    @staticmethod
    def has_overlap(check_in: date, check_out: date, existing: list["Booking"]) -> bool:
        for b in existing:
            if check_in < b.check_out and b.check_in < check_out:
                return True
        return False