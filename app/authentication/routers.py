from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from datetime import datetime, timedelta
from app.authentication.models import User, Session
from app.subscription.models import Subscription, UserSubscription
from app.authentication.schemas import UserRegistrationRequest, Token, LoginRequest
from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
import jwt
from app.authentication.helper import create_access_token, validate_access_token, create_session, validate_session
from config import settings
from passlib.hash import bcrypt
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.authentication.send_mail import send_email_smtp

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 password bearer for token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# load_dotenv()
auth_router = APIRouter()


@auth_router.post("/register", status_code=201)
async def register_user(
        user_data: UserRegistrationRequest, background_tasks: BackgroundTasks
):
    user_email = user_data.email
    # Check if email already exists
    existing_user = await User.find_one({"email": user_email})

    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists.")

    # Get subscription
    subscription = await Subscription.get(user_data.subscription_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found.")

    # Create user record
    user = User(email=user_data.email, source=user_data.source)
    await user.insert()

    # Create UserSubscription record
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=subscription.duration)

    user_subscription = UserSubscription(
        user=user,
        subscription=subscription,
        start_date=start_date,
        end_date=end_date
    )
    await user_subscription.insert()
    # Send activation email
    # Create and return JWT token
    access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
    activation_link = f"{settings.DOMAIN_URL}/activate/{access_token}"
    mail_body = body = f'<p>Click the link to activate your account: <a href="{activation_link}">{activation_link}</a></p>'
    # breakpoint()
    # send_email_smtp(to_email=user_email, body=mail_body, subject="Activate your account")
    background_tasks.add_task(
        send_email_smtp,
        to_email=user_email,
        body=mail_body,
        subject="Activate your account",

    )

    return {"message": "User registered successfully. Please check your email to activate your account."}


# Activation endpoint with JWT token
@auth_router.post("/activate/{access_token}")
async def activate_account(access_token: str, password: str):
    payload = validate_access_token(access_token)
    user = await User.get(payload.get("user_id"))
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if user.is_active:
        raise HTTPException(status_code=400, detail="Account already activated.")

    # Hash and save password
    user.hashed_password = pwd_context.hash(password)
    user.is_active = True
    await user.save()

    # Create and return JWT token
    access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
    return {"message": "Account activated successfully.", "access_token": access_token}



# Login route
@auth_router.post("/login", response_model=Token)
async def login(login_request: LoginRequest):
    user_email = login_request.email
    db_user = await User.find_one({"email": user_email})
    if not db_user or not bcrypt.verify(login_request.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Create token
    access_token = create_access_token(
        data={"sub": user_email, "user_id": db_user.id},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    # Create session
    await create_session(user_email, access_token)
    return {"access_token": f"Bearer {access_token}", "token_type": "bearer"}

# Logout route
@auth_router.post("/logout")
async def logout(token: str):
    # Validate the session based on the token
    session = await validate_session(token)
    # Mark session as inactive (optional, if you don't want to delete the session)
    session.token = None
    await session.save()
    return {"message": "Logged out successfully."}
