from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RegistrationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ATTENDED = "attended"


class Registration(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    registration_id: str
    event_id: str
    user_id: str
    status: RegistrationStatus = RegistrationStatus.PENDING
    checked_in_at: Optional[datetime] = None
    points_awarded: int = 0
    registered_at: datetime
