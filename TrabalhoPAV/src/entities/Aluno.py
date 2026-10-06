# sqlalchemy: biblioteca do python que faz as operações/mapeamento no BD
from sqlalchemy import Column, Integer, String, Date
from src.entities.Base import Base

# Importando a biblioteca inteira
#import sqlalchemy as sql

#Modelagem da classe que mapeia a tabela aluno
class Aluno(Base):
    __tablename__ = "aluno"

    # Columns
    id = Column(
        "id_aluno",
        Integer,
        primary_key=True,
    )
    nome = Column("nome", String(200), nullable=False)
    matricula = Column("matricula", String(50))
    dataNascimento = Column("data_nascimento", Date)
