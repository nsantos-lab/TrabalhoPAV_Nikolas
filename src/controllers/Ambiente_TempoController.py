from flask_restful import Resource, abort, request
from flask_apispec import marshal_with
from flask_apispec.views import MethodResource
from marshmallow import Schema, ValidationError, fields
from sqlalchemy.exc import IntegrityError, OperationalError

from src.services.Ambiente_TempoService import getAmbiente_Tempos, getAmbiente_Tempo, addAmbiente_Tempo, updateAmbiente_Tempo, deleteAmbiente_Tempo
from src.exceptions import ResourceNotFoundError
from src.controllers.responses import load_form, validation_error_response

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
    ambiente = fields.Int(required=True)
    oxigenio = fields.Float(required=True)
    carbonico = fields.Float(required=True)
    poluentes = fields.Float(required=True)
    umidade = fields.Float(required=True)
    densidade = fields.Float(required=True)

class Ambiente_TempoItem(MethodResource, Resource):
    @marshal_with(Ambiente_TempoResponseSchema)
    def get(self, ambiente_tempo_id):
        try:
            # Camada de serviço para obter um ambiente
            ambiente_tempo = getAmbiente_Tempo(ambiente_tempo_id)
            if not ambiente_tempo:
                abort(404, message="Tempo de ambiente não encontrado.")
            return ambiente_tempo, 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    def put(self, ambiente_tempo_id):
        kwargs, error_response = load_form(Ambiente_TempoRequestSchema, request.form)
        if error_response:
            return error_response
        try:
            kwargs["ambiente_id"] = kwargs.pop("ambiente")
            ambiente_tempo = updateAmbiente_Tempo(id=ambiente_tempo_id, **kwargs)
            return Ambiente_TempoResponseSchema().dump(ambiente_tempo), 201
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

    def delete(self, ambiente_tempo_id):
        try:
            # Camada de serviço para excluir um ambiente
            ambiente_tempo = deleteAmbiente_Tempo(ambiente_tempo_id)
            if not ambiente_tempo:
                abort(404, message="Resource not found")
            return 204
        except ResourceNotFoundError as err:
            return {"message": str(err)}, 404
        except IntegrityError as err:
            abort(409, message=str(err.__context__))
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

    def post(self):
        kwargs, error_response = load_form(Ambiente_TempoRequestSchema, request.form)
        if error_response:
            return error_response
        try:
            kwargs["ambiente_id"] = kwargs.pop("ambiente")
            ambiente_tempo = addAmbiente_Tempo(**kwargs)
            return Ambiente_TempoResponseSchema().dump(ambiente_tempo), 201
        except ValidationError as err:
            return validation_error_response(err)
        except IntegrityError as err:
            abort(409, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))
