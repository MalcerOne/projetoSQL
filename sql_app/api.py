'''
Requerimentos
• Usuário pode criar e deletar um carrinho de compras. Pode também alterar sua composição:
adicionar e remover produtos. Você pode supor que já existe uma tabela de usuários, e que
eles são identificados (chave primária) por um ID inteiro.
• Criar produto, consultar inventário de produtos, alterar produto, remover produto do
inventário.
'''

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========User===========
@app.post("/users/", response_model=schemas.User)
def criar_usuario(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def obter_todos_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def obter_usuario(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}")
def remover_usuario(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# =========Carrinho===========
@app.get("/cart/{user_id}/", response_model=schemas.Item)
def obter_carrinho(user_id: int, db: Session = Depends(get_db)):
    db_cart = crud.get_cart(db, user_id=user_id)
    if db_cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return db_cart

@app.post("/cart/{user_id}/", response_model=schemas.Item)
def criar_carrinho(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)

@app.delete("/cart/{user_id}/")
def remove_carrinho(user_id: int, db: Session = Depends(get_db)):
    cart = crud.delete_cart(db, userId=user_id)
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found in user")
    return cart

@app.put("/cart/{user_id}/")
def atualiza_carrinho(user_id: int, db: Session = Depends(get_db)):
    cart = crud.get_cart(db, user_id=user_id)
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found in user")

    # Remove o antigo e sobrescreve com o valor atualizado
    itemRemovido = crud.delete_cart(db, userId=user_id)
    return crud.create_user_item(db=db, item=cart, user_id=user_id)


# =========Inventario===========
@app.get("/storage/", response_model=schemas.Storage)
def obter_inventario(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    storage = crud.get_storage(db, skip=skip, limit=limit)
    if storage is None:
        raise HTTPException(status_code=404, detail="Storage is empty.")
    return storage

@app.post("/storage/", response_model=schemas.Storage)
def adicionar_item_ao_inventario(storageItem: schemas.StorageItemCreate, db: Session = Depends(get_db)):
    db_storageItem = crud.get_storage_item_by_name(db, product_name=storageItem.product_name)
    if db_storageItem:
        raise HTTPException(status_code=400, detail="Produto ja existe no inventario.")
    return crud.add_item_to_storage(storageItem)

@app.delete("/storage/")
def remove_item_do_inventario(storageItem: schemas.Storage, db: Session = Depends(get_db)):
    product = crud.delete_item_from_storage(db, product_id=storageItem.id)
    if product is None:
        raise HTTPException(status_code=404, detail="Item not found in inventory")
    return product

@app.put("/storage/")
def atualiza_item_do_inventario(storageItem: schemas.Storage, db: Session = Depends(get_db)):
    db_storageItem = crud.get_storage_item_by_name(db, product_name=storageItem.product_name)
    if db_storageItem is None:
        raise HTTPException(status_code=404, detail="Item not found in inventory")

    # Remove o antigo e sobrescreve com o valor atualizado
    itemRemovido = crud.delete_item_from_storage(db, product_id=db_storageItem.id)
    return crud.add_item_to_storage(db_storageItem)
