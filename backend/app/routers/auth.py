"""
Custom email + password authentication router.
Replaces Firebase Auth entirely.

Collections used:
  auth_users/{uid}  — stores { email, password_hash, name, created_at }
  users/{uid}       — stores the public UserProfile (created atomically on register)

Security notes:
  - Passwords are hashed with bcrypt (cost 12) via passlib.
  - Timing-safe login: a dummy hash is always verified even when email not found,
    preventing user-enumeration via response timing.
  - JWTs are signed HS256 with the JWT_SECRET_KEY from settings.
  - Tokens expire after JWT_EXPIRE_MINUTES (default: 7 days).
"""

import uuid
from datetime import datetime, timezone

from app.config import settings
from app.firebase import get_firestore_client
from app.models.auth import LoginRequest, RegisterRequest, TokenResponse
from fastapi import APIRouter, HTTPException, status
from jose import jwt
from passlib.context import CryptContext

router = APIRouter()

# bcrypt password hashing context
_pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pre-computed dummy hash — used to keep login timing constant when email not found.
# This prevents an attacker from enumerating valid emails via response time.
_DUMMY_HASH = _pwd_ctx.hash("dummy_timing_password_ecobyte")


def _create_access_token(uid: str, email: str, name: str) -> str:
    """Mint a signed JWT containing uid, email, name, and expiry."""
    now = datetime.now(timezone.utc)
    expire = now.timestamp() + settings.jwt_expire_minutes * 60
    payload = {
        "sub": uid,
        "email": email,
        "name": name,
        "iat": int(now.timestamp()),
        "exp": int(expire),
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest):
    """
    Create a new account.
    1. Check email uniqueness (query auth_users by email field).
    2. Hash password with bcrypt.
    3. Atomically batch-write auth record + blank user profile.
    4. Return a JWT so the user is immediately logged in.
    """
    db = get_firestore_client()

    # Check if email already registered
    existing = await db.collection("auth_users").where("email", "==", body.email).limit(1).get()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    uid = str(uuid.uuid4())
    password_hash = _pwd_ctx.hash(body.password)
    now = datetime.now(timezone.utc)

    # Atomic batch: create auth record + bare user profile together.
    # If either write fails the whole batch rolls back.
    batch = db.batch()

    auth_ref = db.collection("auth_users").document(uid)
    batch.set(auth_ref, {
        "uid": uid,
        "email": body.email,
        "password_hash": password_hash,
        "name": body.name,
        "created_at": now,
    })

    profile_ref = db.collection("users").document(uid)
    batch.set(profile_ref, {
        "uid": uid,
        "name": body.name,
        "email": body.email,
        "contact": body.email,
        "area": "",
        "bio": "",
        "interests": [],
        "post_count": 0,
        "follower_count": 0,
        "following_count": 0,
        "total_points": 0,
        "joined_community_ids": [],
        "rank": 0,
        "trust_score": 0.0,
        "created_at": now,
        # Flag: profile is not yet completed (user still needs onboarding)
        "onboarding_complete": False,
    })

    await batch.commit()

    token = _create_access_token(uid=uid, email=body.email, name=body.name)
    return TokenResponse(access_token=token, uid=uid, email=body.email, name=body.name)


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest):
    """
    Authenticate with email + password.
    Always runs bcrypt verify (even if email not found) to prevent timing attacks.
    Returns a JWT on success.
    """
    db = get_firestore_client()

    # Look up the auth record by email
    results = await db.collection("auth_users").where("email", "==", body.email).limit(1).get()

    if results:
        auth_doc = results[0].to_dict()
        stored_hash = auth_doc["password_hash"]
        is_valid = _pwd_ctx.verify(body.password, stored_hash)
    else:
        # Email not found — still run bcrypt to keep timing constant
        _pwd_ctx.verify(body.password, _DUMMY_HASH)
        is_valid = False

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    uid = auth_doc["uid"]
    name = auth_doc.get("name", "")
    token = _create_access_token(uid=uid, email=body.email, name=name)
    return TokenResponse(access_token=token, uid=uid, email=body.email, name=name)
