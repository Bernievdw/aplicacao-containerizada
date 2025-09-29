from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.backend.deps import get_db, get_current_user
from app.backend.crud import crud
from app.backend.schemas.schemas import MovementCreate, MovementRead
from datetime import date

router = APIRouter(prefix="/api/movements", tags=["movements"], dependencies=[Depends(get_current_user)])

@router.post("", response_model=MovementRead)
def create_movement(movement_in: MovementCreate, db: Session = Depends(get_db)):
    client = crud.get_client(db, movement_in.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    if movement_in.type not in ("deposit", "withdrawal"):
        raise HTTPException(status_code=400, detail="type must be deposit or withdrawal")
    movement = crud.create_movement(db, movement_in)
    return movement

@router.get("", response_model=list[MovementRead])
def list_movements(client_id: Optional[int] = None, start_date: Optional[date] = None, end_date: Optional[date] = None, db: Session = Depends(get_db)):
    return crud.list_movements(db, client_id, start_date, end_date)
