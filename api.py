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

INVENTORY = {
                'nescau'  : {'qtd': 6, 'preco': 3, 'descricao': 'blabla'} ,
                'repolho' : {'qtd': 2, 'preco': 22, 'descricao': 'blabla'},
            }

CART = {
        '123': {
                'nescau'  : {'qtd': 6, 'preco': 3, 'descricao': 'blabla'},
                'awp'     : {'qtd': 6, 'preco': 3, 'descricao': 'que ota?'}
               },

        '456': {
                'banana'  : {'qtd': 2, 'preco': 23, 'descricao': 'blabla'},
                'glock'   : {'qtd': 5, 'preco': 15, 'descricao': 'que ota?'}
               }
       }

#Ping route to check if server is up and running
@app.get('/')
async def root():
    return {'message': 'Hello from your carrinho de compras'}