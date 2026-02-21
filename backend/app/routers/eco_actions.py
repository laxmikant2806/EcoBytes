from datetime import datetime
import uuid
from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, status
from firebase_admin import storage
from google.cloud import firestore

from app.dependencies import CurrentUser
from app.firebase import get_firestore_client
from app.models.eco_action import EcoAction, ActionCategory, VerificationStatus

router = APIRouter()

ACTIONS_COLLECTION = "eco_actions"

@router.get("/")
async def list_eco_actions(user: CurrentUser):
    """List eco actions for the current user."""
    db = get_firestore_client()
    # Fetch all user actions and sort in memory to avoid needing a composite index
    docs = db.collection(ACTIONS_COLLECTION).where("author_id", "==", user["uid"]).stream()
    
    actions = []
    async for doc in docs:
        actions.append(doc.to_dict())
        
    actions.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return {"items": actions}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_eco_action(
    user: CurrentUser,
    category: ActionCategory = Form(...),
    quantity: float = Form(...),
    quantity_unit: str = Form(...),
    description: Optional[str] = Form(None),
    community_id: Optional[str] = Form(None),
    file: UploadFile = File(...)
):
    """
    Submit a new eco action with an image or video.
    Stores metadata in Firestore and uploads the file to Firebase Storage.
    """
    db = get_firestore_client()
    bucket = storage.bucket()
    
    action_id = str(uuid.uuid4())
    file_ext = file.filename.split(".")[-1] if file.filename else "bin"
    file_path = f"eco_actions/{user['uid']}/{action_id}.{file_ext}"
    
    # Upload file
    blob = bucket.blob(file_path)
    blob.upload_from_string(
        await file.read(),
        content_type=file.content_type
    )
    blob.make_public()
    file_url = blob.public_url
    
    is_video = file.content_type.startswith("video/") if file.content_type else False
    
    new_action = EcoAction(
        id=action_id,
        author_id=user["uid"],
        category=category,
        quantity=quantity,
        quantity_unit=quantity_unit,
        description=description,
        community_id=community_id,
        image_url=file_url if not is_video else None,
        video_url=file_url if is_video else None,
        timestamp=datetime.utcnow(),
        verification_status=VerificationStatus.PENDING,
        points_earned=0.0 # Will be updated after verification
    )
    
    await db.collection(ACTIONS_COLLECTION).document(action_id).set(new_action.model_dump())
    
    # Update user's post count
    user_ref = db.collection("users").document(user["uid"])
    await user_ref.update({
        "post_count": firestore.Increment(1)
    })
    
    return new_action


@router.get("/{action_id}")
async def get_eco_action(action_id: str, user: CurrentUser):
    """Return a single eco action by ID."""
    db = get_firestore_client()
    doc = await db.collection(ACTIONS_COLLECTION).document(action_id).get()
    
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Action not found")
        
    return doc.to_dict()
