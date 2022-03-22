'''
Requerimentos
• Usuário pode criar e deletar um carrinho de compras. Pode também alterar sua composição:
adicionar e remover produtos. Você pode supor que já existe uma tabela de usuários, e que
eles são identificados (chave primária) por um ID inteiro.
• Criar produto, consultar inventário de produtos, alterar produto, remover produto do
inventário.
'''

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel



tags_metadata = [
    {
        "name": "inventory",
        "description": "Operations with inventory",
    },
    {
        "name": "cart",
        "description": "Operations with the client cart",
    },
]

app = FastAPI(
        title="CarrinhoCRUD",
        description="The best API in the world!",
        version="0.0.1",
        openapi_tags=tags_metadata,
        contact={
            "name": "Daniel Delattre | Rafael Malcer",
        },
        license_info={
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        },
    )

class Info(BaseModel):
    description: str | None = None
    price: float
    qtd: int

class Product(BaseModel):
    name: str
    info: Info

    class Config:
        schema_extra = {
                        "example": 
                            {
                                "name": "SKIN DE AWP RED DRAGON",
                                "info": {
                                    "description": "An optional description",
                                    "price": 100000000000,
                                    "qtd": 1
                                }
                            }
                        }

class Item_name(BaseModel):
    name: str

class Cart(BaseModel):
    cart: list[Product]

    class Config:
        schema_extra = {
                          "example": 
                              { 'cart': 
                                  [
                                      {"name": "limao1", "info": {"qtd": 6, "price": 3, "description": "blabla"}},
                                      {"name": "limao2", "info": {"qtd": 6, "price": 3, "description": "blabla"}},
                                      {"name": "limao3", "info": {"qtd": 6, "price": 3, "description": "blabla"}}
                                  ]
                              }
                        } 

app = FastAPI()


INVENTORY = {
                'nescau'  : {'qtd': 6, 'preco': 3, 'descricao': 'blabla'} ,
                'repolho' : {'qtd': 2, 'preco': 22, 'descricao': 'blabla'},
            }

CART = {
        '123': {
                'nescau'  : {'qtd': 6, 'preco': 3, 'descricao': 'blabla'},
                'awp'  : {'qtd': 6, 'preco': 3, 'descricao': 'que ota?'}
               },

        '456': {
                'banana'  : {'qtd': 2, 'preco': 23, 'descricao': 'blabla'},
                'glock'  : {'qtd': 5, 'preco': 15, 'descricao': 'que ota?'}
               }
       }


#Ping route to check if server is up and running
@app.get('/')
async def root():
    return {'message': 'Hello from your carrinho de compras'}



#Routes to interact with products cart
@app.post('/cart/{user_id}', tags=['cart'])
async def create_cart(user_id):
    CART[user_id] = {}
    return {'message': f'Carrinho user_id: {user_id} criado com sucesso!', 
            'carrinho': CART[user_id]}

@app.put('/cart/{user_id}', tags=['cart'])
async def update_cart(user_id, cart: Cart):
    if user_id not in CART:
        return {'message': 'Usuario nao tem carrinho!'}
    
    cart = cart.cart

    carrinho = {}
    for product in cart:
        p_name = product.name
        p_info = product.info
        carrinho[p_name] = p_info

    CART[user_id] = carrinho
    return {'message': f'Carrinho user_id: {user_id} atualizado com sucesso!', 
            'carrinho': CART[user_id]}

@app.delete('/cart/{user_id}', tags=['cart'])
async def delete_cart(user_id):
    if user_id not in CART:
        return {'message': 'Usuario nao tem carrinho!'}
    del CART[user_id]
    return {'message': f'Carrinho user_id: {user_id} deletado com sucesso!'}

@app.get('/cart/{user_id}', tags=['cart'])
async def get_products_from_cart(user_id):
    if user_id not in CART:
        return {'message': 'Usuario nao tem carrinho!'}
    return {'carrinho': CART[user_id]}



#Routes to interact with the inventory
@app.get('/inventory/', tags=['inventory'])
async def get_all_items_from_inventory():
    return {'inventory': INVENTORY}

@app.post('/inventory/', tags=['inventory'])
async def create_item_in_inventory(product: Product):
    p_name = product.name
    p_info = product.info
    INVENTORY[p_name] = p_info
    return {'inventory': INVENTORY}

@app.put('/inventory/', tags=['inventory'])
async def update_item_in_inventory(product: Product):
    p_name = product.name
    p_info = product.info

    if p_name not in INVENTORY:
        return {'message': f'product: {p_name} not in inventory!', 'inventory': INVENTORY}

    INVENTORY[p_name] = p_info

    return {'message': f'product: {p_name} updated successfully!', 'inventory': INVENTORY}

@app.delete('/inventory/', tags=['inventory'])
async def delete_item_from_inventory(item: Item_name):
    item_name = item.name
    del INVENTORY[item_name]
    return {'inventory': INVENTORY}



    







