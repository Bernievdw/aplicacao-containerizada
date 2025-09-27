from typing import Optional, List
from datetime import date
from pydantic import BaseModel, EmailStr

# Auth
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None

# User schemas
class UserCreate(BaseModel):
    name: Optional[str]
    email: EmailStr
    password: str
    is_active: Optional[bool] = True

class UserRead(BaseModel):
    id: int
    name: Optional[str]
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True

# Client schemas
class ClientCreate(BaseModel):
    name: str
    email: Optional[EmailStr]
    is_active: Optional[bool] = True

class ClientRead(BaseModel):
    id: int
    name: str
    email: Optional[EmailStr]
    is_active: bool
    created_at: Optional[str]

    class Config:
        orm_mode = True

# Asset schemas
class AssetCreate(BaseModel):
    ticker: str
    name: Optional[str]
    exchange: Optional[str]
    currency: Optional[str]

class AssetRead(BaseModel):
    id: int
    ticker: str
    name: Optional[str]
    exchange: Optional[str]
    currency: Optional[str]

    class Config:
        orm_mode = True

# Allocation schemas
class AllocationCreate(BaseModel):
    client_id: int
    asset_id: Optional[int]
    ticker: Optional[str]
    quantity: float
    buy_price: float
    buy_date: date

class AllocationRead(BaseModel):
    id: int
    client_id: int
    asset_id: int
    quantity: float
    buy_price: float
    buy_date: date
    created_at: Optional[str]

    class Config:
        orm_mode = True

# Movement schemas
class MovementCreate(BaseModel):
    client_id: int
    type: str  # deposit|withdrawal
    amount: float
    date: date
    note: Optional[str] = None

class MovementRead(BaseModel):
    id: int
    client_id: int
    type: str
    amount: float
    date: date
    note: Optional[str]

    class Config:
        orm_mode = True
