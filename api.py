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

app = FastAPI()

class Info(BaseModel):
    description: str | None = None
    price: float
    qtd: int

class Product(BaseModel):
    name: str
    info: Info

class Item_name(BaseModel):
    name: str

class Cart(BaseModel):
    cart: dict(Product)

app = FastAPI()


CARRINHOS = {}
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


#Routes to interact with products cart
@app.post('/cart/{user_id}')
async def create_cart(user_id):
    CART[user_id] = {}
    return {'message': f'Carrinho user_id: {user_id} criado com sucesso!', 
            'carrinho': CART[user_id]}

@app.put('/cart/{user_id}')
async def update_cart(user_id, cart: Cart):
    if user_id not in CART:
        return {'message': 'Usuario nao tem carrinho!'}

    CART[user_id] = cart
    return {'message': f'Carrinho user_id: {user_id} atualizado com sucesso!', 
            'carrinho': CART[user_id]}

@app.delete('/cart/{user_id}')
async def delete_cart(user_id):
    if user_id not in CART:
        return {'message': 'Usuario nao tem carrinho!'}
    del CART[user_id]
    return {'message': f'Carrinho user_id: {user_id} deletado com sucesso!'}

@app.get('/cart/{user_id}')
async def get_products_from_cart(user_id):
    if user_id not in CART:
        return {'message': 'Usuario nao tem carrinho!'}
    return {'carrinho': CART[user_id]}


#Ping route to check if server is up and running
@app.get('/')
async def root():
    return {'message': 'Hello from your carrinho de compras'}


#Routes to interact with the inventory
@app.get('/inventory/')
async def get_all_items_from_inventory():
    return {'inventory': INVENTORY}

@app.post('/inventory/')
async def create_item_in_inventory(product: Product):
    p_name = product.name
    p_info = product.info
    INVENTORY[p_name] = p_info
    return {'inventory': INVENTORY}

@app.put('/inventory/')
async def update_item_in_inventory(product: Product):
    p_name = product.name
    p_info = product.info

    if p_name not in INVENTORY:
        return {'message': f'product: {p_name} not in inventory!', 'inventory': INVENTORY}

    INVENTORY[p_name] = p_info

    return {'message': f'product: {p_name} updated successfully!', 'inventory': INVENTORY}

@app.delete('/inventory/')
async def delete_item_from_inventory(item: Item_name):
    item_name = item.name
    del INVENTORY[item_name]
    return {'inventory': INVENTORY}



    







