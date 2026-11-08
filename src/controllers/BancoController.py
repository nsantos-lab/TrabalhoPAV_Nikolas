from flask_restful import Resource, abort, request
from flask_apispec import marshal_with
from flask_apispec.views import MethodResource
from marshmallow import Schema, ValidationError, fields
from sqlalchemy.exc import IntegrityError, OperationalError

from src.services.BancoService import getBancos, getBanco, addBanco, updateBanco, deleteBanco, getBancoByCliente
from src.exceptions import ResourceNotFoundError
from src.controllers.responses import load_form, validation_error_response

class BancoResponseSchema(Schema): # Transforma dict em json
    id_banco = fields.Int()
    id_cliente = fields.Int()
    dinheiro = fields.Float()
    senha = fields.Str()

class BancoRequestSchema(Schema): # Transforma json em dict
    id_cliente = fields.Int(required=True)
    dinheiro = fields.Float(required=True)
    senha = fields.Str(required=True)

class BancoItem(MethodResource, Resource):
    @marshal_with(BancoResponseSchema)
    def get(self, id_banco):
        try:
            # Camada de serviço para obter um cliente
            banco = getBanco(id_banco)
            if not banco:
                abort(404, message="Banco não encontrado.")
            return banco, 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    def put(self, id_banco):
        kwargs, error_response = load_form(BancoRequestSchema, request.form)
        if error_response:
            return error_response
        try:
            banco = updateBanco(id_banco=id_banco, **kwargs)
            return BancoResponseSchema().dump(banco), 201
        except ValidationError as err:
            return validation_error_response(err)
        except ResourceNotFoundError as err:
            return {"message": str(err)}, 404
        except IntegrityError as err:
            abort(409, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))


    def delete(self, id_banco):
        try:
            # Camada de serviço para excluir um banco
            banco = deleteBanco(id_banco)
            if not banco:
                abort(404, message="Resource not found")
            return 204
        except ResourceNotFoundError as err:
            return {"message": str(err)}, 404
        except IntegrityError as err:
            abort(409, message=str(err.__context__))
        except OperationalError:
            abort(500, message="Internal Server Error")

class BancoByCliente(MethodResource, Resource):
    @marshal_with(BancoResponseSchema)
    def get(self, id_cliente):
        try:
            banco = getBancoByCliente(id_cliente)
            if not banco:
                abort(404, message="Banco para o cliente não encontrado.")
            return banco, 200
        except OperationalError:
            abort(500, message="Internal Server Error")

class BancoList(MethodResource, Resource):
    # Transforma o objeto em json
    @marshal_with(BancoResponseSchema(many=True))
    def get(self):
        try:
            # Camada de serviço para obter a lista de bancos
            return getBancos(), 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    def post(self):
        kwargs, error_response = load_form(BancoRequestSchema, request.form)
        if error_response:
            return error_response
        try:
            banco = addBanco(**kwargs)
            return BancoResponseSchema().dump(banco), 201
        except ValidationError as err:
            return validation_error_response(err)
        except IntegrityError as err:
            abort(409, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))
