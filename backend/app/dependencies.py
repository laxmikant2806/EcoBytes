"""
FastAPI dependency: verify custom JWT (replaces Firebase Auth token verification).

All 7 existing routers use `CurrentUser` — the type alias is unchanged,
so no router files need to be touched.
"""

from typing import Annotated

from app.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError, JWTError, jwt

security = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> dict:
    """
    Verify the JWT from the Authorization: Bearer <token> header.
    Returns a dict with at least: { uid, email, name }.
    Raises 401 if the token is missing, invalid, or expired.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        uid: str | None = payload.get("sub")
        email: str | None = payload.get("email")
        name: str | None = payload.get("name", "")
        if not uid or not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing subject or email.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"uid": uid, "email": email, "name": name}
    except ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {exc}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


# Convenience alias — use this in router signatures for clean code:
#   async def some_endpoint(user: CurrentUser): ...
CurrentUser = Annotated[dict, Depends(get_current_user)]
