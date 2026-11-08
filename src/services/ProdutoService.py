from src.repositories.ProdutoRepository import get_lista_produtos, get_produto, add_produto, update_produto, delete_produto
from src.entities.produto import Produto
from marshmallow import ValidationError
from math import isfinite
import re

# Implementação das regras de negócio no cadastro do produto. CRUD

def getProdutos():
    return get_lista_produtos()

def getProduto(produto_id):
    return get_produto(produto_id)

def _validar_produto(id_ambiente, tipo, preco, potencia):
    if id_ambiente is None or id_ambiente < 0:
        raise ValidationError({"id_ambiente": "Ambiente ID must not be null or negative."})
    if tipo is None or not re.fullmatch(r"[A-Z]{3}", tipo):
        raise ValidationError({"tipo": "Tipo must contain exactly 3 uppercase letters."})
    if preco is None or not isfinite(preco) or preco < 0:
        raise ValidationError({"preco": "Preço must be a finite, non-negative number."})
    if potencia is None or not isfinite(potencia) or potencia <= 0:
        raise ValidationError({"potencia": "Potência must be a finite, positive number."})

def addProduto(id_ambiente: int, tipo: str, preco: float, potencia: float) -> Produto:
    _validar_produto(id_ambiente, tipo, preco, potencia)
    
    return add_produto(id_ambiente=id_ambiente, tipo=tipo, preco=preco, potencia=potencia)

def updateProduto(id: int, id_ambiente: int, tipo: str, preco: float, potencia: float):
    _validar_produto(id_ambiente, tipo, preco, potencia)
    return update_produto(id=id, id_ambiente=id_ambiente, tipo=tipo, preco=preco, potencia=potencia)

def deleteProduto(produto_id):
    return delete_produto(produto_id)
