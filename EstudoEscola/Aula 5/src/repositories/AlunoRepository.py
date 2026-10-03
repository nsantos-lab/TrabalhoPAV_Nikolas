from src.entities.Aluno import Aluno
from src.entities.Base import db

def get_lista_alunos():
    """
    Get all alunos stored in the database.

    Returns:
        alunos (Aluno) -- contains all alunos registered.
    """
    # SELECT * FROM ALUNO
    # Lista de alunos
    alunos = db.session.query(Aluno).all()
    
    return alunos

def get_aluno(aluno_id):
    """ /* comentário de múltiplas linhas  */
    Get one aluno stored in the database.

    Returns:
        aluno (Aluno) -- find one aluno registered.
    """
    # SELECT * FROM ALUNO WHERE id=aluno_id
    aluno = db.session.query(Aluno).get(aluno_id)
    
    return aluno

def add_aluno(id: int, nome: str, matricula: str):
    aluno = Aluno(id=id, nome=nome, matricula=matricula)
    
    # INSERT INTO Aluno values (id, nome, matricula)
    db.session.add(aluno)

    # Confirma a execução
    db.session.commit()

    return aluno

def update_aluno(nome: str, id: int, matricula: float) -> Aluno:
    """
    Insert a Aluno in the database.
    """
    # Verifica se o aluno existe
    aluno = db.session.query(Aluno).get(id)

    if(not aluno):
        raise Exception
    
    aluno.nome = nome
    aluno.matricula = matricula

    db.session.commit()

    return aluno

def delete_aluno(aluno_id):
    """
    Delete one aluno stored in the database.

    Returns:
        aluno (Aluno) -- delete one aluno registered.
    """
    aluno = db.session.query(Aluno).get(aluno_id)
    db.session.delete(aluno)
    db.session.commit()
    return aluno