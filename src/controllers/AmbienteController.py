from flask_restful import Resource, abort, request
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm.exc import UnmappedInstanceError

from src.services.AmbienteService import getAmbientes, getAmbiente, addAmbiente, updateAmbiente, deleteAmbiente

class AmbienteResponseSchema(Schema): # Transforma dict em json
    id = fields.Int()
    cliente = fields.Int()
    oxigenio = fields.Float()
    carbonico = fields.Float()
    poluentes = fields.Float()
    umidade = fields.Float()
    densidade = fields.Float()
    dados_publicos = fields.Bool()
    data_cadastro = fields.DateTime()

class AmbienteRequestSchema(Schema): # Transforma json em dict
    id = fields.Int()
    cliente = fields.Int()
    oxigenio = fields.Float()
    carbonico = fields.Float()
    poluentes = fields.Float()
    umidade = fields.Float()
    densidade = fields.Float()
    dados_publicos = fields.Bool()
    data_cadastro = fields.DateTime()

class AmbienteItem(MethodResource, Resource):
    @marshal_with(AmbienteResponseSchema)
    def get(self, ambiente_id):
        try:
            # Camada de serviço para obter um ambiente
            ambiente = getAmbiente(ambiente_id)
            if not ambiente:
                abort(404, message="Resource not found")
            return ambiente, 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    @use_kwargs(AmbienteRequestSchema, location=("form"))
    @marshal_with(AmbienteResponseSchema)
    def put(self, ambiente_id, **kwargs):
        try:
            # Camada de serviço para atualizar um ambiente
            kwargs["cliente_id"] = kwargs.pop("cliente")
            ambiente = updateAmbiente(id=ambiente_id, **kwargs)
            return ambiente, 201
        except IntegrityError as err:
            abort(500, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))
        #finally:
        #

    def delete(self, ambiente_id):
        try:
            # Camada de serviço para excluir um ambiente
            ambiente = deleteAmbiente(ambiente_id)
            if not ambiente:
                abort(404, message="Resource not found")
            return 204
        except OperationalError:
            abort(500, message="Internal Server Error")

class AmbienteList(MethodResource, Resource):
    # Transforma o objeto em json
    @marshal_with(AmbienteResponseSchema(many=True))
    def get(self):
        try:
            # Camada de serviço para obter a lista de ambientes
            return getAmbientes(), 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    @use_kwargs(AmbienteRequestSchema, location=("form"))
    @marshal_with(AmbienteResponseSchema)
    def post(self, **kwargs):
        try:
            # Camada de serviço para inserir um ambiente
            kwargs["cliente_id"] = kwargs.pop("cliente")
            ambiente = addAmbiente(**kwargs)
            return ambiente, 201
        except IntegrityError as err:
            abort(500, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))
