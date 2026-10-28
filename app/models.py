import sqlalchemy
from app.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String(255), unique=True, index=True, nullable=False)
    phone = sqlalchemy.Column(sqlalchemy.String(20), nullable=True)
    company = sqlalchemy.Column(sqlalchemy.String(150), nullable=True)
    enquiry = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    status = sqlalchemy.Column(sqlalchemy.String(20), default="New", nullable=False)

    # AI-generated lead insights
    ai_classification = sqlalchemy.Column(sqlalchemy.String(20), nullable=True)
    ai_reason = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    ai_suggested_action = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
