from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class EventCreate(BaseModel):
    event_title: str
    event_description: str
    community_id: Optional[str] = None
    is_city_event: bool = False
    city: Optional[str] = None
    location_name: str
    lat: float
    lng: float
    geohash: str = Field(description="Geohash of lat/lng for proximity queries")
    event_type: str = Field(description="e.g. 'cleanup', 'tree_planting', 'awareness'")
    start_time: datetime
    end_time: datetime
    max_attendees: int = Field(gt=0)
    requires_approval: bool = False

    @model_validator(mode="after")
    def end_after_start(self) -> "EventCreate":
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class Event(EventCreate):
    model_config = ConfigDict(populate_by_name=True)

    event_id: str
    current_attendees: int = 0
    created_by: str = Field(description="UID of the user who created the event")
    created_at: datetime
