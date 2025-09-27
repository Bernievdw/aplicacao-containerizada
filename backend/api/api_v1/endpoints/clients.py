from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app import crud
from app.schemas import ClientCreate, ClientRead
from fastapi import status

router = APIRouter(prefix="/api/clients", tags=["clients"], dependencies=[Depends(get_current_user)])

@router.get("", response_model=list[ClientRead])
def list_clients(q: Optional[str] = None, is_active: Optional[bool] = None, page: int = 1, per_page: int = 25, db: Session = Depends(get_db)):
    offset = (page - 1) * per_page
    clients = crud.get_clients(db, q=q, is_active=is_active, offset=offset, limit=per_page)
    return clients

@router.post("", response_model=ClientRead, status_code=status.HTTP_201_CREATED)
def create_client(client_in: ClientCreate, db: Session = Depends(get_db)):
    client = crud.create_client(db, client_in)
    return client

@router.get("/{client_id}", response_model=ClientRead)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = crud.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.put("/{client_id}", response_model=ClientRead)
def update_client(client_id: int, client_in: ClientCreate, db: Session = Depends(get_db)):
    client = crud.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    updated = crud.update_client(db, client, client_in.dict(exclude_unset=True))
    return updated

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = crud.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    crud.delete_client(db, client)
    return {}
