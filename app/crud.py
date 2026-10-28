from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app import models, schemas


def create_lead(db: Session, lead: schemas.LeadCreate):
    new_lead = models.Lead(**lead.model_dump())

    try:
        db.add(new_lead)
        db.commit()
        db.refresh(new_lead)
        return new_lead
    except IntegrityError:
        db.rollback()
        raise ValueError("A lead with this email already exists.")


def get_leads(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: str | None = None,
    status: str | None = None
):
    query = db.query(models.Lead)

    # Search by name, email, or company.
    if search:
        search_term = f"%{search}%"

        query = query.filter(
            models.Lead.name.ilike(search_term)
            | models.Lead.email.ilike(search_term)
            | models.Lead.company.ilike(search_term)
        )

    # Filter by lead status.
    if status:
        query = query.filter(models.Lead.status == status)

    # Apply pagination and return the results.
    return query.offset(skip).limit(limit).all()


def get_lead(db: Session, lead_id: int):
    return db.query(models.Lead).filter(
        models.Lead.id == lead_id
    ).first()


def update_lead(db: Session, lead_id: int, lead_data: schemas.LeadUpdate):
    db_lead = get_lead(db, lead_id)

    if db_lead is None:
        return None

    updates = lead_data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(db_lead, field, value)

    try:
        db.commit()
        db.refresh(db_lead)
        return db_lead
    except IntegrityError:
        db.rollback()
        raise ValueError("A lead with this email already exists.")


def update_lead_status(db: Session, lead_id: int, status: str):
    db_lead = get_lead(db, lead_id)

    if db_lead is None:
        return None

    db_lead.status = status
    db.commit()
    db.refresh(db_lead)

    return db_lead


def delete_lead(db: Session, lead_id: int):
    db_lead = get_lead(db, lead_id)

    if db_lead is None:
        return False

    db.delete(db_lead)
    db.commit()

    return True