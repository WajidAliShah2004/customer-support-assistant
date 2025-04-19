from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from src.api.deps import get_current_user
from src.db.session import get_db
from src.models.models import User
from src.schemas.ticket import MessageCreate, Ticket, TicketCreate, TicketUpdate
from src.services.ai import ai_service
from src.services.ticket import ticket_service

router = APIRouter()


@router.get("/", response_model=List[Ticket])
def get_tickets(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Retrieve tickets for the current user.
    """
    tickets = ticket_service.get_by_user(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    return tickets


@router.post("/", response_model=Ticket)
def create_ticket(
    *,
    db: Session = Depends(get_db),
    ticket_in: TicketCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Create new ticket.
    """
    ticket = ticket_service.create_with_user(
        db=db, obj_in=ticket_in, user_id=current_user.id
    )
    return ticket


@router.get("/{ticket_id}", response_model=Ticket)
def get_ticket(
    *,
    db: Session = Depends(get_db),
    ticket_id: UUID,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get ticket by ID.
    """
    ticket = ticket_service.get(db=db, id=ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if ticket.user_id != current_user.id and not current_user.role == "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return ticket


@router.post("/{ticket_id}/messages", response_model=Ticket)
def add_message(
    *,
    db: Session = Depends(get_db),
    ticket_id: UUID,
    message_in: MessageCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Add a message to a ticket.
    """
    ticket = ticket_service.get(db=db, id=ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if ticket.user_id != current_user.id and not current_user.role == "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    ticket_service.add_message(db=db, ticket_id=ticket_id, message_in=message_in)
    return ticket_service.get(db=db, id=ticket_id)


@router.get("/{ticket_id}/ai-response")
async def get_ai_response(
    *,
    db: Session = Depends(get_db),
    ticket_id: UUID,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Stream AI response for a ticket.
    """
    ticket = ticket_service.get(db=db, id=ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if ticket.user_id != current_user.id and not current_user.role == "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    async def generate():
        async for chunk in ai_service.generate_response(ticket, ticket.messages):
            yield f"data: {chunk}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    ) 