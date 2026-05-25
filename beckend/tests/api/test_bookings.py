from datetime import date, timedelta
import uuid

def test_create_booking_success(client, db_session):
    # Create apartment first
    from app.models.apartment import Apartment
    apt = Apartment(
        id=uuid.uuid4(),
        title="Test Apt",
        address="Test St, 1",
        price_per_day=5000,
        photos=[],
        owner_phone="+79991234567"
    )
    db_session.add(apt)
    db_session.commit()
    
    response = client.post("/api/bookings", json={
        "apartment_id": str(apt.id),
        "guest_name": "Артём",
        "guest_phone": "+79990000000",
        "check_in": (date.today() + timedelta(days=1)).isoformat(),
        "check_out": (date.today() + timedelta(days=3)).isoformat()
    })
    assert response.status_code == 201
    data = response.json()
    assert data["guest_name"] == "Артём"

def test_create_booking_overlap(client, db_session):
    from app.models.apartment import Apartment
    from app.models.booking import Booking
    apt = Apartment(
        id=uuid.uuid4(),
        title="Test", address="Test", price_per_day=1000,
        photos=[], owner_phone="+79991234567"
    )
    db_session.add(apt)
    db_session.commit()
    
    # Existing booking
    existing = Booking(
        apartment_id=apt.id,
        guest_name="Other", guest_phone="+79991111111",
        check_in=date.today() + timedelta(days=1),
        check_out=date.today() + timedelta(days=5)
    )
    db_session.add(existing)
    db_session.commit()
    
    # Try overlapping
    response = client.post("/api/bookings", json={
        "apartment_id": str(apt.id),
        "guest_name": "Артём",
        "guest_phone": "+79990000000",
        "check_in": (date.today() + timedelta(days=3)).isoformat(),
        "check_out": (date.today() + timedelta(days=6)).isoformat()
    })
    assert response.status_code == 409

def test_create_booking_invalid_phone(client, db_session):
    from app.models.apartment import Apartment
    apt = Apartment(
        id=uuid.uuid4(),
        title="Test", address="Test", price_per_day=1000,
        photos=[], owner_phone="+79991234567"
    )
    db_session.add(apt)
    db_session.commit()
    
    response = client.post("/api/bookings", json={
        "apartment_id": str(apt.id),
        "guest_name": "Артём",
        "guest_phone": "invalid",
        "check_in": (date.today() + timedelta(days=1)).isoformat(),
        "check_out": (date.today() + timedelta(days=3)).isoformat()
    })
    assert response.status_code == 400