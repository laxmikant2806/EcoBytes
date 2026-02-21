from fastapi import APIRouter, HTTPException, status
from google.cloud import firestore

from app.dependencies import CurrentUser
from app.firebase import get_firestore_client

router = APIRouter()

REWARDS_COLLECTION = "rewards"

@router.get("/")
async def list_rewards(user: CurrentUser):
    """List active rewards available in the store."""
    db = get_firestore_client()
    docs = db.collection(REWARDS_COLLECTION).where("is_active", "==", True).order_by("points_required").stream()
    
    rewards = []
    async for doc in docs:
        rewards.append(doc.to_dict())
    
    return {"items": rewards}


@router.post("/{reward_id}/redeem")
async def redeem_reward(reward_id: str, user: CurrentUser):
    """
    Redeem a reward using points.
    Uses a Firestore transaction to: check stock, deduct user points, decrement stock,
    create a point_ledger entry, and return the redeem_code.
    """
    db = get_firestore_client()
    
    # Implementation of transaction would go here
    # For now, keeping it simple as a proof of concept
    reward_ref = db.collection(REWARDS_COLLECTION).document(reward_id)
    reward_doc = await reward_ref.get()
    
    if not reward_doc.exists:
        raise HTTPException(status_code=404, detail="Reward not found")
        
    reward_data = reward_doc.to_dict()
    if reward_data.get("stock", 0) <= 0:
        raise HTTPException(status_code=400, detail="Reward out of stock")
        
    # TODO: Deduct points and return code
    return {"status": "success", "message": "Redemption logic pending transaction setup"}
