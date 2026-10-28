from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    company = Column(String(150), nullable=True)
    enquiry = Column(Text, nullable=False)
    status = Column(String(20), default="New", nullable=False)