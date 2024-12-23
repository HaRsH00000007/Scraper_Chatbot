from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from config import settings
from app.authentication.models import User, Session
from app.subscription.models import Subscription, UserSubscription

async def init_db():
    client = AsyncIOMotorClient(settings.MONGODB_URL)

    await init_beanie(
        database=client[settings.DATABASE_NAME],
        document_models=[User, Session, Subscription, UserSubscription]
    )

    if not await Subscription.find_one():
        test_subscription = Subscription(name="Basic", price=9.99, duration=30)
        await test_subscription.insert()
        test_subscription = Subscription(name="Premium", price=29, duration=60)
        await test_subscription.insert()
        test_subscription = Subscription(name="enterprise", price=49, duration=130)
        await test_subscription.insert()


