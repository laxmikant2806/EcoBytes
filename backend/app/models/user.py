from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    name: str
    contact: str = Field(default="", description="Phone number or email for contact")
    area: str = Field(default="", description="City or region the user is based in")
    bio: Optional[str] = None
    interests: list[str] = Field(default_factory=list)


class UserCreate(UserBase):
    uid: str = Field(description="Firebase Auth UID — becomes the Firestore document ID")


class UserProfile(UserBase):
    model_config = ConfigDict(populate_by_name=True)

    uid: str
    post_count: int = 0
    follower_count: int = 0
    following_count: int = 0
    total_points: int = 0
    joined_community_ids: list[str] = Field(default_factory=list)
    rank: int = 0
    trust_score: float = 0.0
    created_at: datetime
    # False until the user completes the onboarding form (name, area, contact, interests).
    # Used by the frontend to decide whether to route to /onboarding or /dashboard.
    onboarding_complete: bool = False


class UserUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    area: Optional[str] = None
    interests: Optional[list[str]] = None
    contact: Optional[str] = None
