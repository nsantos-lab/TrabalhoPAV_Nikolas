from flask_restful import Resource, abort, request
from flask_apispec import marshal_with
from flask_apispec.views import MethodResource
from marshmallow import Schema, ValidationError, fields
from sqlalchemy.exc import IntegrityError, OperationalError

from src.services.AmbienteService import getAmbientes, getAmbiente, addAmbiente, updateAmbiente, deleteAmbiente
from src.exceptions import ResourceNotFoundError
from src.controllers.responses import load_form, validation_error_response

class AmbienteResponseSchema(Schema): # Transforma dict em json
    id = fields.Int()
    cliente = fields.Int()
    oxigenio = fields.Float()
    carbonico = fields.Float()
    poluentes = fields.Float()
    umidade = fields.Float()
    temperatura = fields.Float()
    dados_publicos = fields.Bool()
    data_cadastro = fields.DateTime()

class AmbienteRequestSchema(Schema): # Transforma json em dict
    cliente = fields.Int(required=True)
    oxigenio = fields.Float(required=True)
    carbonico = fields.Float(required=True)
    poluentes = fields.Float(required=True)
    umidade = fields.Float(required=True)
    temperatura = fields.Float(required=True)
    dados_publicos = fields.Bool(required=True)

class AmbienteItem(MethodResource, Resource):
    @marshal_with(AmbienteResponseSchema)
    def get(self, ambiente_id):
        try:
            # Camada de serviço para obter um ambiente
            ambiente = getAmbiente(ambiente_id)
            if not ambiente:
                abort(404, message="Ambiente não encontrado.")
            return ambiente, 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    def put(self, ambiente_id):
        kwargs, error_response = load_form(AmbienteRequestSchema, request.form)
        if error_response:
            return error_response
        try:
            kwargs["cliente_id"] = kwargs.pop("cliente")
            ambiente = updateAmbiente(id=ambiente_id, **kwargs)
            return AmbienteResponseSchema().dump(ambiente), 201
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

    def delete(self, ambiente_id):
        try:
            # Camada de serviço para excluir um ambiente
            ambiente = deleteAmbiente(ambiente_id)
            if not ambiente:
                abort(404, message="Resource not found")
            return 204
        except ResourceNotFoundError as err:
            return {"message": str(err)}, 404
        except IntegrityError as err:
            abort(409, message=str(err.__context__))
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

    def post(self):
        kwargs, error_response = load_form(AmbienteRequestSchema, request.form)
        if error_response:
            return error_response
        try:
            kwargs["cliente_id"] = kwargs.pop("cliente")
            ambiente = addAmbiente(**kwargs)
            return AmbienteResponseSchema().dump(ambiente), 201
        except ValidationError as err:
            return validation_error_response(err)
        except IntegrityError as err:
            abort(409, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))
