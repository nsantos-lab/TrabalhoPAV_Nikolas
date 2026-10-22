from repositories.ClienteRepository import get_lista_clientes, get_cliente, add_cliente, update_cliente, delete_cliente
from entities.cliente import Cliente
from datetime import date

# Implementação das regras de negócio no cadastro do cliente. CRUD

def getClientes():
    return get_lista_clientes()

def getCliente(cliente_id):
    return get_cliente(cliente_id)

def addCliente(nome: str, cpf: str, email: str, telefone: str, dados_publicos: bool, data_nascimento: date) -> Cliente:
    if(nome is None or nome == ''):
        raise ValueError("Nome must not be null.")
    if(cpf is None or cpf == ''):
        raise ValueError("CPF must not be null.")
    if(email is None or email == ''):
        raise ValueError("Email must not be null.")
    
    return add_cliente(nome, cpf, email, telefone, dados_publicos, data_nascimento)

def updateCliente(id: int, nome: str, cpf: str, email: str, telefone: str, dados_publicos: bool, data_nascimento: date):
    return update_cliente(id=id, nome=nome, cpf=cpf, email=email, telefone=telefone, dados_publicos=dados_publicos, data_nascimento=data_nascimento)

def deleteCliente(cliente_id):
    return delete_cliente(cliente_id)
