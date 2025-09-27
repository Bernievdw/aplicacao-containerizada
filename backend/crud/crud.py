from sqlmodel import select
from sqlalchemy.exc import NoResultFound
from app import models
from sqlmodel import Session
from typing import Optional, List
import yfinance as yf

# Users
def get_user_by_email(session: Session, email: str) -> Optional[models.User]:
    return session.exec(select(models.User).where(models.User.email == email)).first()

def create_user(session: Session, *, name: str | None, email: str, password_hash: str, is_active: bool = True):
    user = models.User(name=name, email=email, password_hash=password_hash, is_active=is_active)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Clients
def get_clients(session: Session, q: Optional[str] = None, is_active: Optional[bool] = None, offset: int = 0, limit: int = 25) -> List[models.Client]:
    stmt = select(models.Client)
    if q:
        q_like = f"%{q}%"
        stmt = stmt.where((models.Client.name.ilike(q_like)) | (models.Client.email.ilike(q_like)))
    if is_active is not None:
        stmt = stmt.where(models.Client.is_active == is_active)
    stmt = stmt.offset(offset).limit(limit)
    return session.exec(stmt).all()

def get_client(session: Session, client_id: int):
    return session.get(models.Client, client_id)

def create_client(session: Session, client_in):
    client = models.Client.from_orm(client_in)
    session.add(client)
    session.commit()
    session.refresh(client)
    return client

def update_client(session: Session, client: models.Client, data: dict):
    for k, v in data.items():
        setattr(client, k, v)
    session.add(client)
    session.commit()
    session.refresh(client)
    return client

def delete_client(session: Session, client: models.Client):
    session.delete(client)
    session.commit()
    return True

# Assets: import via yfinance
def get_asset_by_ticker(session: Session, ticker: str):
    return session.exec(select(models.Asset).where(models.Asset.ticker == ticker.upper())).first()

def create_or_update_asset(session: Session, ticker: str):
    ticker = ticker.upper()
    asset = get_asset_by_ticker(session, ticker)
    info = None
    try:
        tk = yf.Ticker(ticker)
        info = tk.info
    except Exception:
        info = None
    name = info.get("longName") if info else None
    exchange = info.get("exchange") if info else None
    currency = info.get("currency") if info else None
    if asset:
        asset.name = name or asset.name
        asset.exchange = exchange or asset.exchange
        asset.currency = currency or asset.currency
        session.add(asset)
    else:
        asset = models.Asset(ticker=ticker, name=name, exchange=exchange, currency=currency)
        session.add(asset)
    session.commit()
    session.refresh(asset)
    return asset

def list_assets(session: Session, offset=0, limit=50):
    return session.exec(select(models.Asset).offset(offset).limit(limit)).all()

# Allocations
def create_allocation(session: Session, allocation_in):
    # if ticker provided, ensure asset exists
    if allocation_in.ticker and not allocation_in.asset_id:
        asset = get_asset_by_ticker(session, allocation_in.ticker)
        if not asset:
            asset = create_or_update_asset(session, allocation_in.ticker)
        allocation_in.asset_id = asset.id
    allocation = models.Allocation(client_id=allocation_in.client_id,
                                   asset_id=allocation_in.asset_id,
                                   quantity=allocation_in.quantity,
                                   buy_price=allocation_in.buy_price,
                                   buy_date=allocation_in.buy_date)
    session.add(allocation)
    session.commit()
    session.refresh(allocation)
    return allocation

def list_allocations_by_client(session: Session, client_id: int):
    return session.exec(select(models.Allocation).where(models.Allocation.client_id == client_id)).all()

# Movements
def create_movement(session: Session, movement_in):
    movement = models.Movement(client_id=movement_in.client_id,
                               type=movement_in.type,
                               amount=movement_in.amount,
                               date=movement_in.date,
                               note=movement_in.note)
    session.add(movement)
    session.commit()
    session.refresh(movement)
    return movement

def list_movements(session: Session, client_id: Optional[int] = None, start_date=None, end_date=None):
    stmt = select(models.Movement)
    if client_id:
        stmt = stmt.where(models.Movement.client_id == client_id)
    if start_date:
        stmt = stmt.where(models.Movement.date >= start_date)
    if end_date:
        stmt = stmt.where(models.Movement.date <= end_date)
    return session.exec(stmt).all()

# Reports
from sqlalchemy import func, select as sa_select

def report_captacao_total(session: Session, start_date=None, end_date=None):
    stmt = sa_select(
        models.Movement.type,
        func.sum(models.Movement.amount).label("total")
    )
    if start_date:
        stmt = stmt.where(models.Movement.date >= start_date)
    if end_date:
        stmt = stmt.where(models.Movement.date <= end_date)
    stmt = stmt.group_by(models.Movement.type)
    res = session.exec(stmt).all()
    # return deposit_total - withdrawal_total
    totals = {"deposit": 0.0, "withdrawal": 0.0}
    for t, total in res:
        totals[t] = float(total or 0.0)
    return totals["deposit"] - totals["withdrawal"]

def report_captacao_by_client(session: Session, client_id: int, start_date=None, end_date=None):
    stmt = sa_select(
        models.Movement.type,
        func.sum(models.Movement.amount).label("total")
    ).where(models.Movement.client_id == client_id)
    if start_date:
        stmt = stmt.where(models.Movement.date >= start_date)
    if end_date:
        stmt = stmt.where(models.Movement.date <= end_date)
    stmt = stmt.group_by(models.Movement.type)
    res = session.exec(stmt).all()
    totals = {"deposit": 0.0, "withdrawal": 0.0}
    for t, total in res:
        totals[t] = float(total or 0.0)
    return totals["deposit"] - totals["withdrawal"]
