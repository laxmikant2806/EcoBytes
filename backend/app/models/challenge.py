from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Challenge(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    description: str
    category: str = Field(description="Maps to ActionCategory enum values")
    target_quantity: float = Field(gt=0)
    target_unit: str = Field(description="e.g. 'trees', 'kg', 'km'")
    duration_days: int = Field(gt=0)
    bonus_points: float = Field(ge=0)
    badge_id: Optional[str] = None
    is_active: bool = True


class ChallengeCreate(BaseModel):
    title: str
    description: str
    category: str
    target_quantity: float = Field(gt=0)
    target_unit: str
    duration_days: int = Field(gt=0)
    bonus_points: float = Field(ge=0)
    badge_id: Optional[str] = None
