from flask_restful import Resource, abort, request
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm.exc import UnmappedInstanceError

from src.services.Ambiente_TempoService import getAmbiente_Tempos, getAmbiente_Tempo, addAmbiente_Tempo, updateAmbiente_Tempo, deleteAmbiente_Tempo

class Ambiente_TempoResponseSchema(Schema): # Transforma dict em json
    id = fields.Int()
    ambiente = fields.Int(attribute="id_ambiente")
    oxigenio = fields.Float()
    carbonico = fields.Float()
    poluentes = fields.Float()
    umidade = fields.Float()
    densidade = fields.Float()
    data_cadastro = fields.DateTime()

class Ambiente_TempoRequestSchema(Schema): # Transforma json em dict
    id = fields.Int()
    ambiente = fields.Int()
    oxigenio = fields.Float()
    carbonico = fields.Float()
    poluentes = fields.Float()
    umidade = fields.Float()
    densidade = fields.Float()
    data_cadastro = fields.DateTime()

class Ambiente_TempoItem(MethodResource, Resource):
    @marshal_with(Ambiente_TempoResponseSchema)
    def get(self, ambiente_tempo_id):
        try:
            # Camada de serviço para obter um ambiente
            ambiente_tempo = getAmbiente_Tempo(ambiente_tempo_id)
            if not ambiente_tempo:
                abort(404, message="Resource not found")
            return ambiente_tempo, 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    @use_kwargs(Ambiente_TempoRequestSchema, location=("form"))
    @marshal_with(Ambiente_TempoResponseSchema)
    def put(self, ambiente_tempo_id, **kwargs):
        try:
            # Camada de serviço para atualizar um ambiente
            kwargs["ambiente_id"] = kwargs.pop("ambiente")
            ambiente_tempo = updateAmbiente_Tempo(id=ambiente_tempo_id, **kwargs)
            return ambiente_tempo, 201
        except IntegrityError as err:
            abort(500, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))
        #finally:
        #

    def delete(self, ambiente_tempo_id):
        try:
            # Camada de serviço para excluir um ambiente
            ambiente_tempo = deleteAmbiente_Tempo(ambiente_tempo_id)
            if not ambiente_tempo:
                abort(404, message="Resource not found")
            return 204
        except OperationalError:
            abort(500, message="Internal Server Error")

class Ambiente_TempoList(MethodResource, Resource):
    # Transforma o objeto em json
    @marshal_with(Ambiente_TempoResponseSchema(many=True))
    def get(self):
        try:
            # Camada de serviço para obter a lista de ambientes
            return getAmbiente_Tempos(), 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    @use_kwargs(Ambiente_TempoRequestSchema, location=("form"))
    @marshal_with(Ambiente_TempoResponseSchema)
    def post(self, **kwargs):
        try:
            # Camada de serviço para inserir um ambiente
            kwargs["ambiente_id"] = kwargs.pop("ambiente")
            ambiente_tempo = addAmbiente_Tempo(**kwargs)
            return ambiente_tempo, 201
        except IntegrityError as err:
            abort(500, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))
