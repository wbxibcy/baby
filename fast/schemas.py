from pydantic import BaseModel, Field
from typing import Optional, List

class LoginRequest(BaseModel):
    account: str
    password: str

class MeRequest(BaseModel):
    user_id: int
    name: str
    nickname: str
    gender: str
    account: str
    phone: str
    avatar: Optional[str]

class MeUpdateRequest(BaseModel):
    uid: int = Field(..., description="User ID")
    name: Optional[str] = Field(None, description="Name")
    nickname: Optional[str] = Field(None, description="Nickname")
    gender: Optional[str] = Field(None, description="Gender")
    account: Optional[str] = Field(None, description="Account")
    phone: Optional[str] = Field(None, description="Phone")
    avatar: Optional[bytes] = Field(None, description="Avatar")

class MeUpdateResponse(BaseModel):
    name: str
    nickname: Optional[str] = None
    gender: Optional[str] = None
    account: Optional[str] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None

    class Config:
        orm_mode = True

class DishResponse(BaseModel):
    did: int
    name: str
    image: Optional[bytes] = Field(None, description="image")

class IngredientItem(BaseModel):
    name: str
    quantity: float
    unit: str

class IngredientRequest(BaseModel):
    uid: int
    did: int
    ingredients: List[IngredientItem]