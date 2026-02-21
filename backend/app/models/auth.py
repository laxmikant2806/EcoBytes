"""
Request/response models for the custom email+password auth system.
These are NOT stored in Firestore directly — they are only used for
the /auth/register and /auth/login request/response shapes.

Credentials (hashed password) are stored in the `auth_users` Firestore collection.
User profiles are stored in the `users` Firestore collection.
"""

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, description="Minimum 8 characters")
    name: str = Field(min_length=1, max_length=100)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    uid: str
    email: str
    name: str
