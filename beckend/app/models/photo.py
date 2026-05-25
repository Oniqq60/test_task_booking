import uuid
from sqlalchemy import LargeBinary, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, UUIDMixin

class ApartmentPhoto(Base, UUIDMixin):
    __tablename__ = "apartment_photos"
    
    apartment_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("apartments.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    
    apartment = relationship("Apartment", back_populates="photos")