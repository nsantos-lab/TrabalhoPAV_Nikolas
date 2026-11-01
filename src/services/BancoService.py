from src.repositories.BancoRepository import get_lista_bancos, get_banco, add_banco, update_banco, delete_banco
from src.entities.banco import Banco
from marshmallow import ValidationError
from datetime import date

# Implementação das regras de negócio no cadastro do cliente. CRUD

def getBancos():
    return get_lista_bancos()

def getBanco(id_banco):
    return get_banco(id_banco)

def addBanco(id_cliente: int, dinheiro: float, senha: str) -> Banco:
    if(id_cliente is None):
        raise ValidationError("Cliente ID must not be null.")
    if(dinheiro is None or dinheiro < 0):
        raise ValidationError("Dinheiro must not be null or negative.")
    if(senha is None or senha == ''):
        raise ValidationError("Senha must not be null.")

    return add_banco(id_cliente, dinheiro, senha)

def updateBanco(id_banco: int, id_cliente: int, dinheiro: float, senha: str):
    return update_banco(id_banco=id_banco, id_cliente=id_cliente, dinheiro=dinheiro, senha=senha)

def deleteBanco(id_banco):
    return delete_banco(id_banco)
