from typing import Optional
from uuid import uuid4
from beanie import Document
from pydantic import EmailStr, Field


class User(Document):
    id: str = Field(default_factory=lambda: str(uuid4()))
    email: EmailStr
    hashed_password: Optional[str] = None
    source: str  # e.g., "google", "bing", "instagram", etc.
    is_active: bool = False  # For account activation
    class Settings:
        name = "users"

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john@example.com",
                "source": "google",
                "is_active": False
            }
        }
