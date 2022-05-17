from re import S
from sqlalchemy.orm import Session

import models, schemas

# =========User===========
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(user)
    db.commit()
    return {"text": "Usuario deletado com sucesso! =D"}

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# =========Carrinho===========
def get_cart(db: Session, user_id: int):
    return db.query(models.Item).filter(models.Item.owner_id == user_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_cart(db: Session, userId: int):
    cart = db.query(models.Item).filter(models.Item.owner_id == userId).first()
    db.delete(cart)
    db.commit()
    return {"text": "Carrinho removido com sucesso!"}


# =========Inventario===========
def get_storage(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Storage).offset(skip).limit(limit).all()

def add_item_to_storage(db: Session, storageItem: schemas.Storage):
    db.add(storageItem)
    db.commit()
    db.refresh(storageItem)
    return storageItem

def delete_item_from_storage(db: Session, product_id: int):
    item = db.query(models.Storage).filter(models.Storage.id == product_id).first()
    db.delete(item)
    db.commit()
    return {"text": "Item removido com sucesso do inventario! =D"}

def get_storage_item_by_name(db: Session, product_name: str):
    return db.query(models.Storage).filter(models.Storage.product_name == product_name).first()

