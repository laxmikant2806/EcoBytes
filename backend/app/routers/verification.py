from fastapi import APIRouter

from app.dependencies import CurrentUser

router = APIRouter()


@router.post("/")
async def submit_for_verification(user: CurrentUser):
    """
    Trigger AI verification for an eco action.
    Accepts: action_id + media_url.
    Calls GPT-4o mini vision API, returns structured verdict.
    Updates eco_action verification_status in Firestore.
    """
    # TODO: validate request, call ai_service, update Firestore, award points on approval
    return {"message": "not yet implemented"}


@router.get("/{action_id}/status")
async def get_verification_status(action_id: str, user: CurrentUser):
    """Poll the verification status of an eco action."""
    # TODO: fetch eco_actions/{action_id} and return verification_status + ai_verdict
    return {"message": "not yet implemented", "action_id": action_id}
