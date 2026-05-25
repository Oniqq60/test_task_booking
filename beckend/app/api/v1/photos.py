# app/api/v1/photos.py
import uuid
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.deps import get_db
from app.models.photo import ApartmentPhoto

router = APIRouter()


@router.get("/{photo_id}")
async def get_photo(photo_id: str, db: Session = Depends(get_db)):
    try:
        photo_uuid = uuid.UUID(photo_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid photo ID format")

    stmt = select(ApartmentPhoto).where(ApartmentPhoto.id == photo_uuid)
    photo = db.scalar(stmt)

    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    return Response(
        content=photo.data,
        media_type=photo.content_type,
        headers={"Cache-Control": "public, max-age=31536000, immutable"}
    )