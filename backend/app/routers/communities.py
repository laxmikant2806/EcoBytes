from datetime import datetime
import uuid
from fastapi import APIRouter, HTTPException, status
from google.cloud import firestore

from app.dependencies import CurrentUser
from app.firebase import get_firestore_client
from app.models.community import Community, CommunityCreate

router = APIRouter()

COMMUNITIES_COLLECTION = "communities"

@router.get("/")
async def list_communities(user: CurrentUser):
    """List all communities, ordered by member_count desc."""
    db = get_firestore_client()
    docs = db.collection(COMMUNITIES_COLLECTION).order_by("member_count", direction=firestore.Query.DESCENDING).stream()
    
    communities = []
    async for doc in docs:
        communities.append(doc.to_dict())
    
    return {"items": communities}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_community(body: CommunityCreate, user: CurrentUser):
    """Create a new community. The creating user becomes admin."""
    db = get_firestore_client()
    
    community_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    new_community = Community(
        id=community_id,
        name=body.name,
        type=body.type,
        area_of_work=body.area_of_work,
        description=body.description,
        location=body.location,
        image_url=body.image_url,
        member_count=1,
        members=[user["uid"]],
        admin_id=user["uid"],
        created_at=now
    )
    
    await db.collection(COMMUNITIES_COLLECTION).document(community_id).set(new_community.model_dump())
    
    # Update user's joined communities
    user_ref = db.collection("users").document(user["uid"])
    await user_ref.update({
        "joined_community_ids": firestore.ArrayUnion([community_id])
    })
    
    return new_community


@router.post("/{community_id}/join")
async def join_community(community_id: str, user: CurrentUser):
    """Add the current user to a community's members array."""
    db = get_firestore_client()
    comm_ref = db.collection(COMMUNITIES_COLLECTION).document(community_id)
    comm_doc = await comm_ref.get()
    
    if not comm_doc.exists:
        raise HTTPException(status_code=404, detail="Community not found")
    
    batch = db.batch()
    batch.update(comm_ref, {
        "members": firestore.ArrayUnion([user["uid"]]),
        "member_count": firestore.Increment(1)
    })
    
    user_ref = db.collection("users").document(user["uid"])
    batch.update(user_ref, {
        "joined_community_ids": firestore.ArrayUnion([community_id])
    })
    
    await batch.commit()
    return {"status": "joined", "community_id": community_id}


@router.post("/{community_id}/leave")
async def leave_community(community_id: str, user: CurrentUser):
    """Remove the current user from a community."""
    db = get_firestore_client()
    comm_ref = db.collection(COMMUNITIES_COLLECTION).document(community_id)
    
    batch = db.batch()
    batch.update(comm_ref, {
        "members": firestore.ArrayRemove([user["uid"]]),
        "member_count": firestore.Increment(-1)
    })
    
    user_ref = db.collection("users").document(user["uid"])
    batch.update(user_ref, {
        "joined_community_ids": firestore.ArrayRemove([community_id])
    })
    
    await batch.commit()
    return {"status": "left", "community_id": community_id}


@router.get("/{community_id}")
async def get_community(community_id: str, user: CurrentUser):
    """Return a single community by ID."""
    db = get_firestore_client()
    doc = await db.collection(COMMUNITIES_COLLECTION).document(community_id).get()
    
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Community not found")
        
    return doc.to_dict()
