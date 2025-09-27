from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app import crud
from app.schemas import AssetCreate, AssetRead

router = APIRouter(prefix="/api/assets", tags=["assets"], dependencies=[Depends(get_current_user)])

@router.post("/import", response_model=AssetRead)
def import_asset(body: dict, db: Session = Depends(get_db)):
    tickers = body.get("tickers") or []
    if not tickers:
        raise HTTPException(status_code=400, detail="tickers is required")
    # import first ticker for now; frontend can post one by one
    ticker = tickers[0]
    asset = crud.create_or_update_asset(db, ticker)
    return asset

@router.get("", response_model=list[AssetRead])
def list_assets(page: int = 1, per_page: int = 50, db: Session = Depends(get_db)):
    offset = (page - 1) * per_page
    return crud.list_assets(db, offset=offset, limit=per_page)
