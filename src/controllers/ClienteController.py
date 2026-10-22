import re

from flask_restful import Resource, abort, request
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, ValidationError, fields, validates
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm.exc import UnmappedInstanceError
from src.services.ClienteService import getClientes, getCliente, addCliente, updateCliente, deleteCliente

class ClienteResponseSchema(Schema): # Transforma dict em json
    id = fields.Int()
    nome = fields.Str()
    cpf = fields.Str()
    email = fields.Str()
    telefone = fields.Str()
    dados_publicos = fields.Bool()
    data_nascimento = fields.Date()
    data_cadastro = fields.DateTime()

class ClienteRequestSchema(Schema): # Transforma json em dict
    id = fields.Int()
    nome = fields.Str()
    cpf = fields.Str()
    email = fields.Str()
    telefone = fields.Str()
    dados_publicos = fields.Bool()
    data_nascimento = fields.Date()
    data_cadastro = fields.DateTime()

    @validates("nome")
    def validate_name(self, value):
        if not re.match(pattern=r"^[a-zA-Z0-9_\s]+$", string=value):
            raise ValidationError("Value must contain only alphanumeric and underscore characters.")

class ClienteItem(MethodResource, Resource):
    @marshal_with(ClienteResponseSchema)
    def get(self, cliente_id):
        try:
            # Camada de serviço para obter um cliente
            cliente = getCliente(cliente_id)
            if not cliente:
                abort(404, message="Resource not found")
            return cliente, 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    @use_kwargs(ClienteRequestSchema, location=("form"))
    @marshal_with(ClienteResponseSchema)
    def put(self, cliente_id, **kwargs):
        try:
            # Camada de serviço para atualizar um cliente
            cliente = updateCliente(id=cliente_id, **kwargs)
            return cliente, 201
        except IntegrityError as err:
            abort(500, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))
        #finally:
        #

    def delete(self, cliente_id):
        try:
            # Camada de serviço para excluir um cliente
            cliente = deleteCliente(cliente_id)
            if not cliente:
                abort(404, message="Resource not found")
            return 204
        except OperationalError:
            abort(500, message="Internal Server Error")

class ClienteList(MethodResource, Resource):
    # Transforma o objeto em json
    @marshal_with(ClienteResponseSchema(many=True))
    def get(self):
        try:
            # Camada de serviço para obter a lista de clientes
            return getClientes(), 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    @use_kwargs(ClienteRequestSchema, location=("form"))
    @marshal_with(ClienteResponseSchema)
    def post(self, **kwargs):
        try:
            # Camada de serviço para inserir um cliente
            cliente = addCliente(**kwargs)
            return cliente, 201
        except IntegrityError as err:
            abort(500, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))
