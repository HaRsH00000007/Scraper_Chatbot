from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class SubscriptionCreate(BaseModel):
    name: str
    price: float
    duration: int

class SubscriptionResponse(SubscriptionCreate):
    id: str

    class Config:
        from_attributes = True


class UserSubscriptionCreate(BaseModel):
    subscription_id: str

class UserSubscriptionResponse(BaseModel):
    id: str
    user_id: str
    subscription: dict
    start_date: datetime
    end_date: datetime
    is_active: bool

    class Config:
        from_attributes = True
