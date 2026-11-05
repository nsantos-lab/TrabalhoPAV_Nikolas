import re

from flask_restful import Resource, abort, request
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, ValidationError, fields, validates
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm.exc import UnmappedInstanceError

from src.services.BancoService import getBancos, getBanco, addBanco, updateBanco, deleteBanco, getBancoByCliente

class BancoResponseSchema(Schema): # Transforma dict em json
    id_banco = fields.Int()
    id_cliente = fields.Int()
    dinheiro = fields.Float()
    senha = fields.Str()

class BancoRequestSchema(Schema): # Transforma json em dict
    id_banco = fields.Int()
    id_cliente = fields.Int()
    dinheiro = fields.Float()
    senha = fields.Str()

    @validates("id_banco")
    def validate_id_banco(self, value):
        if not re.match(pattern=r"^[0-9]+$", string=value):
            raise ValidationError("Value must contain only numeric characters.")
    @validates("id_cliente")
    def validate_id_cliente(self, value):
        if not re.match(pattern=r"^[0-9]+$", string=value):
            raise ValidationError("Value must contain only numeric characters.")
    @validates("dinheiro")
    def validate_dinheiro(self, value):
        if not re.match(pattern=r"^[0-9]+(\.[0-9]+)?$", string=value):
            raise ValidationError("Value must be a valid decimal number.")

class BancoItem(MethodResource, Resource):
    @marshal_with(BancoResponseSchema)
    def get(self, id_banco):
        try:
            # Camada de serviço para obter um cliente
            banco = getBanco(id_banco)
            if not banco:
                abort(404, message="Resource not found")
            return banco, 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    @use_kwargs(BancoRequestSchema, location=("form"))
    @marshal_with(BancoResponseSchema)
    def put(self, id_banco, **kwargs):
        try:
            # Camada de serviço para atualizar um banco
            banco = updateBanco(id_banco=id_banco, **kwargs)
            return banco, 201
        except IntegrityError as err:
            abort(500, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))


    def delete(self, id_banco):
        try:
            # Camada de serviço para excluir um banco
            banco = deleteBanco(id_banco)
            if not banco:
                abort(404, message="Resource not found")
            return 204
        except OperationalError:
            abort(500, message="Internal Server Error")

class BancoByCliente(MethodResource, Resource):
    @marshal_with(BancoResponseSchema)
    def get(self, id_cliente):
        try:
            banco = getBancoByCliente(id_cliente)
            if not banco:
                abort(404, message="Resource not found")
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

    @use_kwargs(BancoRequestSchema, location=("form"))
    @marshal_with(BancoResponseSchema)
    def post(self, **kwargs):
        try:
            # Camada de serviço para inserir um banco
            banco = addBanco(**kwargs)
            return banco, 201
        except IntegrityError as err:
            abort(500, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))
