import re

from flask_restful import Resource, abort, request
from flask_apispec import marshal_with, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, ValidationError, fields, validates
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm.exc import UnmappedInstanceError
from src.services.AlunoService import deleteAluno, updateAluno, getAlunos, getAluno, addAluno

class AlunoResponseSchema(Schema): # Transforma dict em json
    id = fields.Int()
    nome = fields.Str()
    matricula = fields.Str()

class AlunoRequestSchema(Schema): # Transforma json em dict
    id = fields.Int()
    nome = fields.Str()
    matricula = fields.Str()
    
    @validates("nome")
    def validate_name(self, value):
        if not re.match(pattern=r"^[a-zA-Z0-9_\s]+$", string=value):
            raise ValidationError(
                "Value must contain only alphanumeric and underscore characters."
            )

class AlunoItem(MethodResource, Resource):
    @marshal_with(AlunoResponseSchema)
    def get(self, aluno_id):
        try:
            # Camada de serviço para obter um aluno
            aluno = getAluno(aluno_id)
            if not aluno:
                abort(404, message="Resource not found")
            return aluno, 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    @use_kwargs(AlunoRequestSchema, location=("form"))
    @marshal_with(AlunoResponseSchema)
    def put(self, aluno_id, **kwargs):
        try:
            # Camada de serviço para atualizar um aluno
            aluno = updateAluno(id=aluno_id, **kwargs)
            return aluno, 201
        except IntegrityError as err:
            abort(500, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))
        #finally:
        #

    def delete(self, aluno_id):
        try:
            # Camada de serviço para excluir um aluno
            aluno = deleteAluno(aluno_id)
            if not aluno:
                abort(404, message="Resource not found")
            return 204
        except OperationalError:
            abort(500, message="Internal Server Error")

class AlunoList(MethodResource, Resource):
    # Transforma o objeto em json
    @marshal_with(AlunoResponseSchema(many=True))
    def get(self):
        try:
            # Camada de serviço para obter a lista de alunos
            return getAlunos(), 200
        except OperationalError:
            abort(500, message="Internal Server Error")

    @use_kwargs(AlunoRequestSchema, location=("form"))
    @marshal_with(AlunoResponseSchema)
    def post(self, **kwargs):
        try:
            # Camada de serviço para inserir um aluno
            aluno = addAluno(**kwargs)
            return aluno, 201
        except IntegrityError as err:
            abort(500, message=str(err.__context__))
        except OperationalError as err:
            abort(500, message=str(err.__context__))
