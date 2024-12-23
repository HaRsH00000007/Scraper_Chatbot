from typing import Optional
from uuid import uuid4
from beanie import Document
from pydantic import EmailStr, Field
from datetime import datetime, timezone



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

class Session(Document):
    id: str = Field(default_factory=lambda: str(uuid4()))  # Unique session ID
    email: EmailStr
    token: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime
    is_active: bool = True

    class Settings:
        name = "sessions"

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john@example.com",
                "token": "some-jwt-token",
                "session_id": "unique-session-id",
                "created_at": "2024-12-24T12:34:56",
                "expires_at": "2024-12-24T14:34:56",
                "is_active": True
            }
        }