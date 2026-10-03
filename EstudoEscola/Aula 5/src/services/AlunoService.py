from src.repositories.AlunoRepository import delete_aluno, update_aluno, add_aluno, get_lista_alunos, get_aluno
from src.entities.Aluno import Aluno
from marshmallow import ValidationError

# Implementação das regras de negócio no cadastro do aluno. CRUD

def getAlunos():
    return get_lista_alunos()

def getAluno(aluno_id):
    return get_aluno(aluno_id)

def addAluno(id: int, nome: str, matricula: str) -> Aluno:
    if(id is None or id == '' or nome is None or nome == ''):
        raise ValidationError(
                "Id and nome must not be null."
            )

    if int(matricula) < 0:
        raise ValidationError(
                "matricula must be positive."
            )
    
    return add_aluno(id, nome, matricula)

def updateAluno(id: int, nome: str, matricula: str):
    return update_aluno(id=id, nome=nome, matricula=matricula)

def deleteAluno(aluno_id):
    return delete_aluno(aluno_id)
