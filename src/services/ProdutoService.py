from src.repositories.ProdutoRepository import get_lista_produtos, get_produto, add_produto, update_produto, delete_produto
from src.entities.produto import Produto
from marshmallow import ValidationError

# Implementação das regras de negócio no cadastro do produto. CRUD

def getProdutos():
    return get_lista_produtos()

def getProduto(produto_id):
    return get_produto(produto_id)

def addProduto(id_ambiente: int, tipo: str, preco: float, potencia: float) -> Produto:
    if(id_ambiente is None or id_ambiente < 0):
        raise ValidationError("Ambiente ID must not be null or negative.")
    if(tipo is None or tipo == ''):
        raise ValidationError("Tipo must not be null or empty.")
    if(preco is None or preco < 0):
        raise ValidationError("Preço must not be null or negative.")
    if(potencia is None or potencia == 0 or potencia < 0):
        raise ValidationError("Potência must not be null, zero or negative.")
    
    return add_produto(id_ambiente=id_ambiente, tipo=tipo, preco=preco, potencia=potencia)

def updateProduto(id: int, id_ambiente: int, tipo: str, preco: float, potencia: float):
    return update_produto(id=id, id_ambiente=id_ambiente, tipo=tipo, preco=preco, potencia=potencia)

def deleteProduto(produto_id):
    return delete_produto(produto_id)
