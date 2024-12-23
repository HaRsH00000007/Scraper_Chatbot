from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
import jwt
from app.authentication.models import Session
from datetime import datetime, timedelta, timezone
from config import settings

# Helper function to create JWT token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


# Helper function to decode and validate JWT token
def validate_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")


# Create session
async def create_session(email: str, token: str):
    expiration = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # Create and save session document
    session = Session(
        email=email,
        token=token,
        created_at=datetime.now(timezone.utc),
        expires_at=expiration,
        is_active=True
    )
    await session.save()  # Save the session to MongoDB

    return session


# Validate session
async def validate_session(token: str):
    # Find the session based on the token
    session = await Session.find_one({"token": token})  # Query using token
    if not session:
        raise HTTPException(status_code=401, detail="Session not found or expired")

    # Check if session is expired
    if session.expires_at.replace(tzinfo=None) < datetime.now(timezone.utc).replace(tzinfo=None):
        # session.delete()  # Delete the expired session
        raise HTTPException(status_code=401, detail="Session expired")

    return session