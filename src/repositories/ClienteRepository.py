from datetime import date
from src.entities.cliente import Cliente
from src.entities.base import db
from src.exceptions import ResourceNotFoundError

def get_lista_clientes():
    clientes = db.session.query(Cliente).all()
    return clientes

def get_cliente(cliente_id):
    cliente = db.session.query(Cliente).get(cliente_id)
    return cliente

def add_cliente(nome: str, cpf: str, email: str, telefone: str, dados_publicos: bool, data_nascimento: date):
    cliente = Cliente(nome=nome, cpf=cpf, email=email, telefone=telefone, dados_publicos=dados_publicos, data_nascimento=data_nascimento)
    # INSERT INTO Cliente values (nome, cpf, email, telefone, dados_publicos, data_nascimento)
    db.session.add(cliente)
    db.session.commit()
    return cliente

def update_cliente(id: int, nome: str, cpf: str, email: str, telefone: str, dados_publicos: bool, data_nascimento: date) -> Cliente:
    cliente = db.session.query(Cliente).get(id)
    if(not cliente):
        raise ResourceNotFoundError("Cliente não encontrado.")

    cliente.nome = nome
    cliente.cpf = cpf
    cliente.email = email
    cliente.telefone = telefone
    cliente.dados_publicos = dados_publicos
    cliente.data_nascimento = data_nascimento

    db.session.commit()
    return cliente

def delete_cliente(cliente_id):
    cliente = db.session.query(Cliente).get(cliente_id)
    if not cliente:
        raise ResourceNotFoundError("Cliente não encontrado.")
    db.session.delete(cliente)
    db.session.commit()
    return cliente