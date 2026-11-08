from flask_restful import Resource, abort, request
from flask_apispec import marshal_with
from flask_apispec.views import MethodResource
import re

from marshmallow import Schema, ValidationError, fields, validates
from sqlalchemy.exc import IntegrityError, OperationalError

from src.services.ClienteService import getClientes, getCliente, addCliente, updateCliente, deleteCliente
from src.exceptions import ResourceNotFoundError
from src.controllers.responses import load_form, validation_error_response

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
    nome = fields.Str(required=True)
    cpf = fields.Str(required=True)
    email = fields.Str(required=True)
    telefone = fields.Str(required=True)
    dados_publicos = fields.Bool(required=True)
    data_nascimento = fields.Date(required=True)

    @validates("nome")
    def validate_name(self, value):
        if not re.fullmatch(r"[a-zA-Z0-9_\s]+", value):
            raise ValidationError("Value must contain only alphanumeric and underscore characters.")
    @validates("cpf")
    def validate_cpf(self, value):
        if not re.fullmatch(r"[0-9]{11}", value):
            raise ValidationError("Value must contain only 11 numeric characters.")
    @validates("email")
    def validate_email(self, value):
        if not re.fullmatch(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.([a-zA-Z0-9-.])+", value):
            raise ValidationError("Value must be in the format email@domain.com")
    @validates("telefone")
    def validate_telefone(self, value):
        if not re.fullmatch(r"[0-9]{11}", value):
            raise ValidationError("Value must contain only 11 numeric characters.")

class ClienteItem(MethodResource, Resource):
    @marshal_with(ClienteResponseSchema)
    def get(self, cliente_id):
        try:
            # Camada de serviço para obter um cliente
            cliente = getCliente(cliente_id)
            if not cliente:
                abort(404, message="Cliente não encontrado.")
            return cliente, 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    def put(self, cliente_id):
        kwargs, error_response = load_form(ClienteRequestSchema, request.form)
        if error_response:
            return error_response
        try:
            cliente = updateCliente(id=cliente_id, **kwargs)
            return ClienteResponseSchema().dump(cliente), 201
        except ValidationError as err:
            return validation_error_response(err)
        except ResourceNotFoundError as err:
            return {"message": str(err)}, 404
        except IntegrityError as err:
            abort(409, message=str(err.__context__))
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
        except ResourceNotFoundError as err:
            return {"message": str(err)}, 404
        except IntegrityError as err:
            abort(409, message=str(err.__context__))

class ClienteList(MethodResource, Resource):
    # Transforma o objeto em json
    @marshal_with(ClienteResponseSchema(many=True))
    def get(self):
        try:
            # Camada de serviço para obter a lista de clientes
            return getClientes(), 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    def post(self):
        kwargs, error_response = load_form(ClienteRequestSchema, request.form)
        if error_response:
            return error_response
        try:
            cliente = addCliente(**kwargs)
            return ClienteResponseSchema().dump(cliente), 201
        except ValidationError as err:
            return validation_error_response(err)
        except IntegrityError as err:
            abort(409, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))
