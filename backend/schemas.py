from pydantic import BaseModel, validator
from typing import Optional, List


class SellerCreate(BaseModel):
    name: str
    phone: str

    @validator("name")
    def name_not_empty(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty")
        return v

    @validator("phone")
    def phone_valid(cls, v):
        v = v.strip().replace(" ", "").replace("-", "")
        digits = v.replace("+", "")
        if not digits.isdigit():
            raise ValueError("Phone must contain only digits")
        if len(digits) < 10:
            raise ValueError("Phone number too short")
        return v


class SellerResponse(BaseModel):
    id: str
    name: str
    phone: str

    class Config:
        from_attributes = True


class MenuItemCreate(BaseModel):
    seller_id: str
    name: str
    price: float
    image_url: Optional[str] = None

    @validator("name")
    def name_not_empty(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Item name cannot be empty")
        return v

    @validator("price")
    def price_positive(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than 0")
        return v


class MenuItemResponse(BaseModel):
    id: int
    seller_id: str
    name: str
    price: float
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class MenuResponse(BaseModel):
    seller: SellerResponse
    items: List[MenuItemResponse]
