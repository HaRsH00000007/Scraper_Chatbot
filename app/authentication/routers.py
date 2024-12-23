from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from datetime import datetime, timedelta
from app.authentication.models import User
from app.subscription.models import Subscription, UserSubscription
from app.authentication.schemas import UserRegistrationRequest
from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
import jwt
from app.authentication.helper import create_access_token, validate_access_token
from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_smtp(to_email: str, subject: str, body: str):
    # SMTP server configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = settings.MAIL_PORT

    # SMTP user configuration
    smtp_username = settings.MAIL_USERNAME
    smtp_password = settings.MAIL_PASSWORD

    if not smtp_username or not smtp_password:
        raise ValueError("SMTP username or password is not set in environment variables")

    # Create the email
    message = MIMEMultipart()
    message["From"] = smtp_username
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)

    except smtplib.SMTPAuthenticationError:
        raise HTTPException(status_code=401, detail="Authentication failed. Check your email credentials.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")


# # Helper to send activation emails
# async def send_activation_email(email: str, link: str):
#     conf = ConnectionConfig(
#         MAIL_USERNAME=os.environ.get("MAIL_USERNAME"),
#         MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD"),
#         MAIL_FROM=os.environ.get("MAIL_FROM"),
#         MAIL_PORT=587,
#         MAIL_SERVER="smtp.gmail.com",
#         MAIL_STARTTLS=True,
#         MAIL_SSL_TLS=False,
#         USE_CREDENTIALS=True
#     )
#     body = f'<p>Click the link to activate your account: <a href="{link}">{link}</a></p>'
#     message = MessageSchema(
#         subject="Activate Your Account",
#         recipients=[email],
#         body=body,
#         subtype="html"
#     )
#     fm = FastMail(conf)
#     await fm.send_message(message)


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
