from typing import Optional
from datetime import datetime, date
from sqlmodel import SQLModel, Field, Relationship

class UserBase(SQLModel):
    name: Optional[str]
    email: str
    is_active: bool = True

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ClientBase(SQLModel):
    name: str
    email: Optional[str]
    is_active: bool = True

class Client(ClientBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    allocations: list["Allocation"] = Relationship(back_populates="client")
    movements: list["Movement"] = Relationship(back_populates="client")

class AssetBase(SQLModel):
    ticker: str
    name: Optional[str]
    exchange: Optional[str]
    currency: Optional[str]

class Asset(AssetBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ticker: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    allocations: list["Allocation"] = Relationship(back_populates="asset")

class AllocationBase(SQLModel):
    quantity: float
    buy_price: float
    buy_date: date

class Allocation(AllocationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.id")
    asset_id: int = Field(foreign_key="asset.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    client: Optional[Client] = Relationship(back_populates="allocations")
    asset: Optional[Asset] = Relationship(back_populates="allocations")

class MovementBase(SQLModel):
    type: str  # deposit | withdrawal
    amount: float
    date: date
    note: Optional[str] = None

class Movement(MovementBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: int = Field(foreign_key="client.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    client: Optional[Client] = Relationship(back_populates="movements")
