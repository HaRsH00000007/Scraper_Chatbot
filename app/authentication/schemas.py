from pydantic import BaseModel, EmailStr
from beanie import Document
from pydantic import EmailStr
from typing import Optional


# class UserBase(BaseModel):
#     email: EmailStr
#     name: str
#
# class UserCreate(UserBase):
#     password: str
#
# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str
#
# class User(UserBase):
#     id: int
#     is_active: bool
#
#     class Config:
#         from_attributes = True
#
# class Token(BaseModel):
#     access_token: str
#     token_type: str




class UserRegistrationRequest(BaseModel):
    email: EmailStr
    subscription_id: str
    source: str  # E.g., "google", "bing", "instagram", "linkedIN"
