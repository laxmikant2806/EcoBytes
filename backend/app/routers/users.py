from fastapi import APIRouter, HTTPException, status

from app.dependencies import CurrentUser
from app.firebase import get_firestore_client
from app.models.user import UserCreate, UserProfile, UserUpdate

router = APIRouter()


@router.post("/", response_model=UserProfile, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, user: CurrentUser):
    """
    Complete onboarding for the authenticated user.
    The uid is taken from the JWT (not the payload) to prevent spoofing.

    Flow:
      - Register creates a bare profile with onboarding_complete=False.
      - This endpoint updates that profile with the onboarding form data
        and sets onboarding_complete=True.
      - If onboarding is already complete, the call is idempotent (returns
        the existing profile unchanged).
    """
    uid = user["uid"]  # always from the verified JWT, not the payload

    db = get_firestore_client()
    doc_ref = db.collection("users").document(uid)
    doc = await doc_ref.get()

    if doc.exists and doc.to_dict().get("onboarding_complete"):
        # Already fully set up — return unchanged (idempotent).
        return UserProfile(**doc.to_dict())

    # Either the bare profile exists (onboarding_complete=False) or it somehow
    # doesn't exist yet. In both cases: write/merge the onboarding data.
    updates = {
        "uid": uid,
        "name": payload.name,
        "contact": payload.contact,
        "area": payload.area,
        "bio": payload.bio or "",
        "interests": payload.interests,
        "onboarding_complete": True,
    }

    if doc.exists:
        await doc_ref.update(updates)
    else:
        # Fallback: bare profile missing (edge case) — create it from scratch.
        from datetime import datetime, timezone  # noqa: PLC0415
        updates.update({
            "post_count": 0,
            "follower_count": 0,
            "following_count": 0,
            "total_points": 0,
            "joined_community_ids": [],
            "rank": 0,
            "trust_score": 0.0,
            "created_at": datetime.now(timezone.utc),
        })
        await doc_ref.set(updates)

    updated_doc = await doc_ref.get()
    return UserProfile(**updated_doc.to_dict())


@router.get("/me", response_model=UserProfile)
async def get_my_profile(user: CurrentUser):
    """Return the current authenticated user's Firestore profile."""
    db = get_firestore_client()
    doc = await db.collection("users").document(user["uid"]).get()

    if not doc.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found. Complete onboarding first.",
        )

    return UserProfile(**doc.to_dict())


@router.patch("/me", response_model=UserProfile)
async def update_my_profile(payload: UserUpdate, user: CurrentUser):
    """Update editable fields on the current user's profile."""
    db = get_firestore_client()
    doc_ref = db.collection("users").document(user["uid"])
    doc = await doc_ref.get()

    if not doc.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found. Complete onboarding first.",
        )

    # Only update fields that were explicitly provided
    updates = payload.model_dump(exclude_none=True)
    if not updates:
        return UserProfile(**doc.to_dict())

    await doc_ref.update(updates)

    updated_doc = await doc_ref.get()
    return UserProfile(**updated_doc.to_dict())
