from fastapi import APIRouter, HTTPException
from typing import List
from app.subscription.models import Subscription
from app.subscription.schemas import SubscriptionResponse

subscription_router = APIRouter()


@subscription_router.get("/subscriptions", response_model=List[SubscriptionResponse])
async def get_all_subscriptions():
    """
    Fetch all subscriptions from the database.
    """
    subscriptions = await Subscription.find_all().to_list()
    if not subscriptions:
        raise HTTPException(status_code=404, detail="No subscriptions found")

    return subscriptions
