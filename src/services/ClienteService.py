from src.repositories.ClienteRepository import get_lista_clientes, get_cliente, add_cliente, update_cliente, delete_cliente
from src.entities.cliente import Cliente
from marshmallow import ValidationError
from datetime import date

# Implementação das regras de negócio no cadastro do cliente. CRUD

def _validar_cliente(nome, cpf, email, telefone, dados_publicos, data_nascimento):
    if nome is None or nome.strip() == "":
        raise ValidationError({"nome": "Nome must not be null or empty."})
    if cpf is None or cpf == "":
        raise ValidationError({"cpf": "CPF must not be null or empty."})
    if email is None or email == "":
        raise ValidationError({"email": "Email must not be null or empty."})
    if telefone is None or telefone == "":
        raise ValidationError({"telefone": "Telefone must not be null or empty."})
    if dados_publicos is None:
        raise ValidationError({"dados_publicos": "Dados públicos must not be null."})
    _validar_data_nascimento(data_nascimento)

def getClientes():
    return get_lista_clientes()

def getCliente(cliente_id):
    return get_cliente(cliente_id)

def _validar_data_nascimento(data_nascimento: date) -> None:
    if data_nascimento is None:
        raise ValidationError({"data_nascimento": "Data de nascimento must not be null."})
    if data_nascimento > date.today():
        raise ValidationError({"data_nascimento": "Data de nascimento must not be in the future."})
    if data_nascimento < date(1906, 1, 1):
        raise ValidationError({"data_nascimento": "Data de nascimento must not be before 1906-01-01."})

def addCliente(nome: str, cpf: str, email: str, telefone: str, dados_publicos: bool, data_nascimento: date) -> Cliente:
    _validar_cliente(nome, cpf, email, telefone, dados_publicos, data_nascimento)
    
    return add_cliente(nome, cpf, email, telefone, dados_publicos, data_nascimento)

def updateCliente(id: int, nome: str, cpf: str, email: str, telefone: str, dados_publicos: bool, data_nascimento: date):
    _validar_cliente(nome, cpf, email, telefone, dados_publicos, data_nascimento)
    return update_cliente(id=id, nome=nome, cpf=cpf, email=email, telefone=telefone, dados_publicos=dados_publicos, data_nascimento=data_nascimento)

def deleteCliente(cliente_id):
    return delete_cliente(cliente_id)
