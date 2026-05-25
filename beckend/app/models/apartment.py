import uuid
from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, UUIDMixin, TimestampMixin

class Apartment(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "apartments"
    
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    price_per_day: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    owner_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    
    bookings = relationship(
        "Booking",
        back_populates="apartment",
        lazy="selectin"
    )
    
    photos = relationship(
        "ApartmentPhoto",
        back_populates="apartment",
        cascade="all, delete-orphan",
        lazy="selectin"
    )