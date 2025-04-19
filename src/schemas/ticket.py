from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class MessageBase(BaseModel):
    content: str
    is_ai: bool = False


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: UUID
    ticket_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class TicketBase(BaseModel):
    title: str
    description: str
    status: str = "open"


class TicketCreate(TicketBase):
    pass


class TicketUpdate(TicketBase):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class Ticket(TicketBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    messages: List[Message] = []

    class Config:
        from_attributes = True 