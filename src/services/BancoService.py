from src.repositories.BancoRepository import get_lista_bancos, get_banco, add_banco, update_banco, delete_banco, get_banco_by_cliente
from src.entities.banco import Banco
from marshmallow import ValidationError
from math import isfinite

# Implementação das regras de negócio no cadastro do cliente. CRUD

def getBancos():
    return get_lista_bancos()

def getBanco(id_banco):
    return get_banco(id_banco)

def _validar_banco(id_cliente, dinheiro, senha):
    if id_cliente is None or id_cliente < 0:
        raise ValidationError({"id_cliente": "Cliente ID must not be null or negative."})
    if dinheiro is None or not isfinite(dinheiro) or dinheiro < 0:
        raise ValidationError({"dinheiro": "Dinheiro must be a finite, non-negative number."})
    if senha is None or senha.strip() == '':
        raise ValidationError({"senha": "Senha must not be null or empty."})

def addBanco(id_cliente: int, dinheiro: float, senha: str) -> Banco:
    _validar_banco(id_cliente, dinheiro, senha)

    return add_banco(id_cliente, dinheiro, senha)

def updateBanco(id_banco: int, id_cliente: int, dinheiro: float, senha: str):
    _validar_banco(id_cliente, dinheiro, senha)
    return update_banco(id_banco=id_banco, id_cliente=id_cliente, dinheiro=dinheiro, senha=senha)

def deleteBanco(id_banco):
    return delete_banco(id_banco)

def getBancoByCliente(id_cliente):
    return get_banco_by_cliente(id_cliente)