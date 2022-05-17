from pydantic import BaseModel

# Carrinho
class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

# User
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True

# Inventario do mercado
class Storage(BaseModel):
    id: int
    product_name: str
    qtd_available: int
    price: float

    class Config:
        orm_mode = True

class StorageItemCreate(BaseModel):
    product_name: str
    qtd_available: int
    price: float