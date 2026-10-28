from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Literal


class LeadCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=20)
    company: str | None = Field(default=None, max_length=150)
    enquiry: str = Field(min_length=5, max_length=2000)


class LeadUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=20)
    company: str | None = Field(default=None, max_length=150)
    enquiry: str | None = Field(default=None, min_length=5, max_length=2000)


class LeadStatusUpdate(BaseModel):
    status: Literal["New", "Contacted", "Qualified", "Converted", "Lost"]


class LeadResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str | None
    company: str | None
    enquiry: str
    status: str

    # AI-generated lead insights
    ai_classification: str | None = None
    ai_reason: str | None = None
    ai_suggested_action: str | None = None

    model_config = ConfigDict(from_attributes=True)


class LeadClassificationResponse(BaseModel):
    classification: Literal["High", "Medium", "Low"]
    reason: str
    suggested_action: str

class LeadClassificationRequest(BaseModel):
    enquiry: str = Field(min_length=5, max_length=2000)
