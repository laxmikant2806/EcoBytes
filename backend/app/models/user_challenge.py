from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserChallengeStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class UserChallenge(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    user_id: str
    challenge_id: str
    progress: float = 0.0
    started_at: datetime
    completed_at: Optional[datetime] = None
    status: UserChallengeStatus = UserChallengeStatus.IN_PROGRESS
