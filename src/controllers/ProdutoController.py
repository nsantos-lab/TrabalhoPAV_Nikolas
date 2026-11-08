import re

from flask_restful import Resource, abort, request
from flask_apispec import marshal_with
from flask_apispec.views import MethodResource
from marshmallow import Schema, ValidationError, fields, validates
from sqlalchemy.exc import IntegrityError, OperationalError

from src.services.ProdutoService import getProdutos, getProduto, addProduto, updateProduto, deleteProduto
from src.exceptions import ResourceNotFoundError
from src.controllers.responses import load_form, validation_error_response

class ProdutoResponseSchema(Schema): # Transforma dict em json
    id = fields.Int()
    id_ambiente = fields.Int()
    tipo = fields.Str()
    preco = fields.Float()
    potencia = fields.Float()

class ProdutoRequestSchema(Schema): # Transforma json em dict
    id_ambiente = fields.Int(required=True)
    tipo = fields.Str(required=True)
    preco = fields.Float(required=True)
    potencia = fields.Float(required=True)

    @validates("id_ambiente")
    def validate_id_ambiente(self, value):
        if value < 0:
            raise ValidationError("Ambiente ID must not be negative.")
    @validates("tipo")
    def validate_tipo(self, value):
        if not re.fullmatch(r"[A-Z]{3}", value):
            raise ValidationError("Tipo must contain exactly 3 uppercase letters.")

class ProdutoItem(MethodResource, Resource):
    @marshal_with(ProdutoResponseSchema)
    def get(self, produto_id):
        try:
            # Camada de serviço para obter um produto
            produto = getProduto(produto_id)
            if not produto:
                abort(404, message="Produto não encontrado.")
            return produto, 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    def put(self, produto_id):
        kwargs, error_response = load_form(ProdutoRequestSchema, request.form)
        if error_response:
            return error_response
        try:
            produto = updateProduto(id=produto_id, **kwargs)
            return ProdutoResponseSchema().dump(produto), 201
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

    def delete(self, produto_id):
        try:
            # Camada de serviço para excluir um produto
            produto = deleteProduto(produto_id)
            if not produto:
                abort(404, message="Resource not found")
            return 204
        except ResourceNotFoundError as err:
            return {"message": str(err)}, 404
        except IntegrityError as err:
            abort(409, message=str(err.__context__))
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

    def post(self):
        kwargs, error_response = load_form(ProdutoRequestSchema, request.form)
        if error_response:
            return error_response
        try:
            produto = addProduto(**kwargs)
            return ProdutoResponseSchema().dump(produto), 201
        except ValidationError as err:
            return validation_error_response(err)
        except IntegrityError as err:
            abort(409, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))
