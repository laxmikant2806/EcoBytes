from typing import Optional

from fastapi import APIRouter, Query

from app.dependencies import CurrentUser
from app.firebase import get_firestore_client

router = APIRouter()


@router.get("/")
async def list_events(
    user: CurrentUser,
    city: Optional[str] = Query(None),
    community_id: Optional[str] = Query(None),
):
    """List upcoming events, optionally filtered by city or community."""
    # TODO: query events where start_time >= now, order by start_time asc
    return {"message": "not yet implemented"}


@router.post("/")
async def create_event(user: CurrentUser):
    """Create a new event. Requires the user to be a community admin."""
    # TODO: validate EventCreate body, compute geohash server-side, write to Firestore
    return {"message": "not yet implemented"}


@router.get("/nearby")
async def get_nearby_events(
    user: CurrentUser,
    lat: float = Query(...),
    lng: float = Query(...),
    radius_km: float = Query(10.0, gt=0, le=100),
):
    """Return events within radius_km of the given coordinates using geohash range queries."""
    # TODO: compute geohash bounding box, query events by geohash prefix range
    return {"message": "not yet implemented", "lat": lat, "lng": lng, "radius_km": radius_km}


@router.get("/{event_id}")
async def get_event(event_id: str, user: CurrentUser):
    """Return a single event by ID."""
    # TODO: fetch events/{event_id}
    return {"message": "not yet implemented", "event_id": event_id}


@router.post("/{event_id}/register")
async def register_for_event(event_id: str, user: CurrentUser):
    """Register the current user for an event."""
    # TODO: check capacity, create registration doc, increment current_attendees
    return {"message": "not yet implemented", "event_id": event_id}
