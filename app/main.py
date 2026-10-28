from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.ai_service import classify_lead
from app.schemas import LeadClassificationResponse

from app.database import engine, Base, get_db
from app import models, schemas, crud

# Create database tables if they do not exist.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LeadFlow API",
    description="A REST API for managing and tracking sales leads.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to LeadFlow!",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# CREATE A LEAD
@app.post(
    "/leads",
    response_model=schemas.LeadResponse,
    status_code=status.HTTP_201_CREATED
)
def create_lead(
    lead: schemas.LeadCreate,
    db: Session = Depends(get_db)
):
    try:
        return crud.create_lead(db, lead)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc)
        )


# GET ALL LEADS

@app.get("/leads", response_model=list[schemas.LeadResponse])
def read_leads(
    skip: int = 0,
    limit: int = 100,
    search: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db)
):
    if skip < 0:
        raise HTTPException(
            status_code=400,
            detail="skip cannot be negative"
        )

    if not 1 <= limit <= 100:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 100"
        )

    allowed_statuses = {
        "New",
        "Contacted",
        "Qualified",
        "Converted",
        "Lost"
    }

    if status is not None and status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid status"
        )

    return crud.get_leads(
        db,
        skip=skip,
        limit=limit,
        search=search,
        status=status
    )

# GET ONE LEAD
@app.get("/leads/{lead_id}", response_model=schemas.LeadResponse)
def read_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = crud.get_lead(db, lead_id)

    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")

    return lead


# UPDATE LEAD DETAILS
@app.put("/leads/{lead_id}", response_model=schemas.LeadResponse)
def update_lead(
    lead_id: int,
    lead_data: schemas.LeadUpdate,
    db: Session = Depends(get_db)
):
    try:
        lead = crud.update_lead(db, lead_id, lead_data)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))

    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")

    return lead


# UPDATE LEAD STATUS
@app.patch("/leads/{lead_id}/status", response_model=schemas.LeadResponse)
def update_lead_status(
    lead_id: int,
    status_data: schemas.LeadStatusUpdate,
    db: Session = Depends(get_db)
):
    lead = crud.update_lead_status(db, lead_id, status_data.status)

    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")

    return lead


# DELETE A LEAD
@app.delete("/leads/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_lead(db, lead_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Lead not found")

    return None



# AI LEAD CLASSIFICATION
@app.post(
    "/leads/classify",
    response_model=schemas.LeadClassificationResponse
)
def classify_lead_enquiry(
    request: schemas.LeadClassificationRequest
):
    try:
        result = classify_lead(request.enquiry)
        return result

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="AI classification failed. Please try again later."
        )