from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.models.models import Message, Ticket
from src.schemas.ticket import MessageCreate, TicketCreate, TicketUpdate
from src.services.base import BaseService


class TicketService(BaseService[Ticket, TicketCreate, TicketUpdate]):
    def get_by_user(
        self, db: Session, *, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Ticket]:
        return (
            db.query(self.model)
            .filter(Ticket.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_user(
        self, db: Session, *, obj_in: TicketCreate, user_id: UUID
    ) -> Ticket:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def add_message(
        self, db: Session, *, ticket_id: UUID, message_in: MessageCreate
    ) -> Message:
        message = Message(**message_in.dict(), ticket_id=ticket_id)
        db.add(message)
        db.commit()
        db.refresh(message)
        return message


ticket_service = TicketService(Ticket) 