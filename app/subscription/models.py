from uuid import uuid4

from beanie import Document, Link
from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional
from app.authentication.models import User
from datetime import datetime

class Subscription(Document):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    price: float
    duration: int  # Duration in days

    class Settings:
        name = "subscriptions"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Premium",
                "price": 29.99,
                "duration": 30  # 30 days subscription
            }
        }

class UserSubscription(Document):
    id: str = Field(default_factory=lambda: str(uuid4()))
    user: Link[User]
    subscription: Link[Subscription]
    start_date: datetime
    end_date: datetime
    is_active: bool = True

    class Settings:
        name = "user_subscriptions"

    class Config:
        json_schema_extra = {
            "example": {
                "start_date": "2024-01-01T00:00:00",
                "end_date": "2024-02-01T00:00:00",
                "is_active": True
            }
        }