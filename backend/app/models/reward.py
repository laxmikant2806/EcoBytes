from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RewardCreate(BaseModel):
    item_name: str
    points_required: float = Field(gt=0)
    stock_count: int = Field(ge=0)
    description: str
    image_url: Optional[str] = None


class Reward(RewardCreate):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    redeem_code: str = Field(description="Unique code generated server-side on creation")
    redeemed_at: Optional[datetime] = None
    is_active: bool = True


class RewardUpdate(BaseModel):
    item_name: Optional[str] = None
    points_required: Optional[float] = None
    stock_count: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
