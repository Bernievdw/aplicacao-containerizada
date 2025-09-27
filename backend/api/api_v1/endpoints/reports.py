from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from app.api.deps import get_db, get_current_user
from app import crud

router = APIRouter(prefix="/api/reports", tags=["reports"], dependencies=[Depends(get_current_user)])

@router.get("/captacao/total")
def captacao_total(start: Optional[date] = None, end: Optional[date] = None, db: Session = Depends(get_db)):
    value = crud.report_captacao_total(db, start, end)
    return {"value": value}

@router.get("/captacao/client/{client_id}")
def captacao_client(client_id: int, start: Optional[date] = None, end: Optional[date] = None, db: Session = Depends(get_db)):
    value = crud.report_captacao_by_client(db, client_id, start, end)
    return {"value": value}
