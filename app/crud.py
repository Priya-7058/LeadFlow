from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.ai_service import classify_lead

from app import models, schemas

def create_lead(db: Session, lead: schemas.LeadCreate):
    new_lead = models.Lead(**lead.model_dump())

    # Generate AI insights before saving the lead.
    try:
        ai_result = classify_lead(lead.enquiry)

        new_lead.ai_classification = ai_result["classification"]
        new_lead.ai_reason = ai_result["reason"]
        new_lead.ai_suggested_action = ai_result["suggested_action"]

    except Exception as exc:
        # Don't lose a lead if the AI service is unavailable.
        print(f"AI classification failed: {exc}")

    # Save the lead, even if AI classification failed.
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

    # Search leads by name, email, or company.
    if search:
        search_term = f"%{search}%"

        query = query.filter(
            models.Lead.name.ilike(search_term)
            | models.Lead.email.ilike(search_term)
            | models.Lead.company.ilike(search_term)
        )

    # Filter leads by their current status.
    if status:
        query = query.filter(models.Lead.status == status)

    # Apply pagination before returning the matching leads.
    return query.offset(skip).limit(limit).all()


def get_lead(db: Session, lead_id: int):
        # Find a lead by ID; return None if it doesn't exist.
    return db.query(models.Lead).filter(
        models.Lead.id == lead_id
    ).first()


def update_lead(db: Session, lead_id: int, lead_data: schemas.LeadUpdate):
        # Retrieve the existing lead before applying updates.
    db_lead = get_lead(db, lead_id)

    if db_lead is None:
        return None
    # Include only fields explicitly provided in the request.
    updates = lead_data.model_dump(exclude_unset=True)

    # Apply each supplied field to the existing database object.
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
        # Retrieve the lead and stop if it doesn't exist.
    db_lead = get_lead(db, lead_id)

    if db_lead is None:
        return None
    
    # Update only the lead's status.
    db_lead.status = status
    db.commit()
    db.refresh(db_lead)

    return db_lead


def delete_lead(db: Session, lead_id: int):
        # Retrieve the lead before attempting deletion. 
    db_lead = get_lead(db, lead_id)

    if db_lead is None:
        return False

    db.delete(db_lead)
    db.commit()

    # Return True to indicate successful deletion.
    return True