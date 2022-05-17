from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(length=128), unique=True, index=True)
    hashed_password = Column(String(length=100))
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "Items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=15), index=True)
    description = Column(String(length=200
    ), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

class Storage(Base):
    __tablename__ = "Storage"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(length=15), index=True)
    qtd_available = Column(Integer, index=True)
    price = Column(Float, index=True)