from fastapi import HTTPException
from app.subscription.models import Subscription

async def get_subscription_by_id(subscription_id: str):
    """
    Fetch a subscription by its ID.
    """
    subscription = await Subscription.get(subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found.")
    return subscription