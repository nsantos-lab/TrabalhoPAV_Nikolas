import re

from flask_restful import Resource, abort, request
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, ValidationError, fields, validates
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm.exc import UnmappedInstanceError

from src.services.ProdutoService import getProdutos, getProduto, addProduto, updateProduto, deleteProduto

class ProdutoResponseSchema(Schema): # Transforma dict em json
    id = fields.Int()
    id_ambiente = fields.Int()
    tipo = fields.Str()
    preco = fields.Float()
    potencia = fields.Float()

class ProdutoRequestSchema(Schema): # Transforma json em dict
    id = fields.Int()
    id_ambiente = fields.Int()
    tipo = fields.Str()
    preco = fields.Float()
    potencia = fields.Float()

    @validates("id")
    def validate_id(self, value):
        if not re.match(pattern=r"^[0-9]+$", string=value):
            raise ValidationError("Value must contain only numeric characters.")
    @validates("id_ambiente")
    def validate_id_ambiente(self, value):
        if not re.match(pattern=r"^[0-9]+$", string=value):
            raise ValidationError("Value must contain only numeric characters.")
    @validates("tipo")
    def validate_tipo(self, value):
        if not re.match(pattern=r"^[A-Z]{3}$", string=value):
            raise ValidationError("Value must contain only 3 uppercase letters.")
    @validates("preco")
    def validate_preco(self, value):
        if not re.match(pattern=r"^[0-9]+(\.[0-9]+)?$", string=value):
            raise ValidationError("Value must be a valid decimal number.")
    @validates("potencia")
    def validate_potencia(self, value):
        if not re.match(pattern=r"^[0-9]+(\.[0-9]+)?$", string=value):
            raise ValidationError("Value must be a valid decimal number.")

class ProdutoItem(MethodResource, Resource):
    @marshal_with(ProdutoResponseSchema)
    def get(self, produto_id):
        try:
            # Camada de serviço para obter um produto
            produto = getProduto(produto_id)
            if not produto:
                abort(404, message="Resource not found")
            return produto, 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    @use_kwargs(ProdutoRequestSchema, location=("form"))
    @marshal_with(ProdutoResponseSchema)
    def put(self, produto_id, **kwargs):
        try:
            # Camada de serviço para atualizar um produto
            produto = updateProduto(id=produto_id, **kwargs)
            return produto, 201
        except IntegrityError as err:
            abort(500, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))
        #finally:
        #

    def delete(self, produto_id):
        try:
            # Camada de serviço para excluir um produto
            produto = deleteProduto(produto_id)
            if not produto:
                abort(404, message="Resource not found")
            return 204
        except OperationalError:
            abort(500, message="Internal Server Error")

class ProdutoList(MethodResource, Resource):
    # Transforma o objeto em json
    @marshal_with(ProdutoResponseSchema(many=True))
    def get(self):
        try:
            # Camada de serviço para obter a lista de produtos
            return getProdutos(), 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    @use_kwargs(ProdutoRequestSchema, location=("form"))
    @marshal_with(ProdutoResponseSchema)
    def post(self, **kwargs):
        try:
            # Camada de serviço para inserir um produto
            produto = addProduto(**kwargs)
            return produto, 201
        except IntegrityError as err:
            abort(500, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))
