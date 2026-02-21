from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PointLedgerEntry(BaseModel):
    """
    Immutable audit record stored in users/{uid}/point_ledger subcollection.
    Positive points = earned. Negative points = redeemed/deducted.
    Never update existing entries — only append.
    """

    model_config = ConfigDict(populate_by_name=True)

    txn_id: str
    action_id: Optional[str] = None
    points: float
    reason: str
    created_at: datetime
