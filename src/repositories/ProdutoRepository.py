from src.entities.produto import Produto
from src.entities.base import db

def get_lista_produtos():
    produtos = db.session.query(Produto).all()
    return produtos

def get_produto(produto_id):
    produto = db.session.query(Produto).get(produto_id)
    return produto

def add_produto(id_ambiente: int, tipo: str, preco: float, potencia: float):
    produto = Produto(id_ambiente=id_ambiente, tipo=tipo, preco=preco, potencia=potencia)
    db.session.add(produto)
    db.session.commit()
    return produto

def update_produto(id: int, id_ambiente: int, tipo: str, preco: float, potencia: float) -> Produto:
    produto = db.session.query(Produto).get(id)
    # Verifica se o produto existe
    if(not produto):
        raise Exception

    produto.id_ambiente = id_ambiente
    produto.tipo = tipo
    produto.preco = preco
    produto.potencia = potencia

    db.session.commit()
    return produto

def delete_produto(produto_id):
    produto = db.session.query(Produto).get(produto_id)
    db.session.delete(produto)
    db.session.commit()
    return produto