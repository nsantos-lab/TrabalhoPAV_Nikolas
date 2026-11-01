from datetime import date
from src.entities.banco import Banco
from src.entities.base import db

def get_lista_bancos():
    bancos = db.session.query(Banco).all()
    return bancos

def get_banco(id_banco):
    banco = db.session.query(Banco).get(id_banco)
    return banco

def add_banco(id_cliente: int, dinheiro: float, senha: str):
    banco = Banco(id_cliente=id_cliente, dinheiro=dinheiro, senha=senha)
    # INSERT INTO Banco values (is_cliente, dinheiro, senha)
    db.session.add(banco)
    db.session.commit()
    return banco

def update_banco(id_banco: int, id_cliente: int, dinheiro: float, senha: str) -> Banco:
    banco = db.session.query(Banco).get(id_banco)
    # Verifica se o cliente existe
    if(not banco):
        raise Exception

    banco.id_cliente = id_cliente
    banco.dinheiro = dinheiro
    banco.senha = senha

    db.session.commit()
    return banco

def delete_banco(id_banco):
    banco = db.session.query(Banco).get(id_banco)
    db.session.delete(banco)
    db.session.commit()
    return banco