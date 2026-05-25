import logging
from pathlib import Path
from typing import List, Optional
import uuid

from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session  # ✅ Исправление: импорт Session

from app.models.photo import ApartmentPhoto
from app.core.config import settings

logger = logging.getLogger("app.services.file_storage")


class FileStorageService:
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    
    def __init__(self, db: Session):
        self.db = db
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
    
    def _validate_file(self, file: UploadFile) -> None:
        """Валидация файла перед сохранением."""
        if file.size and file.size > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Max: {self.MAX_FILE_SIZE // 1024 // 1024}MB"
            )
        
        ext = Path(file.filename or "").suffix.lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type. Allowed: {', '.join(self.ALLOWED_EXTENSIONS)}"
            )
    
    def save_photo(self, file: UploadFile, apartment_id: str) -> ApartmentPhoto:
        """Сохраняет фото и создаёт запись в БД."""
        self._validate_file(file)
        
        ext = Path(file.filename or "").suffix.lower()
        filename = f"{uuid.uuid4().hex}{ext}"
        file_path = self.upload_dir / filename
        
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        
        photo = ApartmentPhoto(
            apartment_id=apartment_id,
            filename=filename,
            content_type=file.content_type or "image/jpeg",
            file_path=str(file_path)
        )
        
        self.db.add(photo)
        self.db.commit()
        self.db.refresh(photo)
        
        logger.info(f"📸 Photo saved: {filename} for apartment {apartment_id}")
        return photo
    
    def get_photo(self, photo_id: uuid.UUID) -> Optional[ApartmentPhoto]:
        """Получает фото по ID."""
        return self.db.query(ApartmentPhoto).filter(ApartmentPhoto.id == photo_id).first()
    
    def delete_photo(self, photo_id: uuid.UUID) -> bool:
        """Удаляет фото с диска и из БД."""
        photo = self.get_photo(photo_id)
        if not photo:
            return False
        
        file_path = Path(photo.file_path)
        if file_path.exists():
            file_path.unlink()
        
        self.db.delete(photo)
        self.db.commit()
        
        logger.info(f"🗑️ Photo deleted: {photo_id}")
        return True