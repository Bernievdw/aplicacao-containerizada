from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app import crud
from app.schemas import AllocationCreate, AllocationRead

router = APIRouter(prefix="/api/allocations", tags=["allocations"], dependencies=[Depends(get_current_user)])

@router.post("", response_model=AllocationRead)
def create_allocation(allocation_in: AllocationCreate, db: Session = Depends(get_db)):
    # ensure client exists
    client = crud.get_client(db, allocation_in.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    allocation = crud.create_allocation(db, allocation_in)
    return allocation

@router.get("/client/{client_id}", response_model=list[AllocationRead])
def list_client_allocations(client_id: int, db: Session = Depends(get_db)):
    return crud.list_allocations_by_client(db, client_id)
