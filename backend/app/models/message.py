from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Message(BaseModel):
    """
    Direct message between two users.
    Firestore document ID convention: "_".join(sorted([uid1, uid2]))
    This allows O(1) lookup of any DM thread without a query.
    """

    model_config = ConfigDict(populate_by_name=True)

    sender_id: str
    receiver_id: str
    content: str
    is_read: bool = False
    sent_at: datetime


class MessageCreate(BaseModel):
    receiver_id: str
    content: str
