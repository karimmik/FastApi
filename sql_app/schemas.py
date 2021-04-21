from typing import List, Optional

from pydantic import BaseModel


class OfferBase(BaseModel):
    price: int
    items_in_stock: int


class OfferCreate(OfferBase):
    pass


class Offer(OfferBase):
    id: int
    product_id: int

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name: str
    description: str


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    offers: List[Offer] = []

    class Config:
        orm_mode = True
