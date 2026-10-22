from flask import Flask
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Date, func
from flask_sqlalchemy import SQLAlchemy
from src.entities.base import Base


class Cliente(Base):
    __tablename__ = "cliente"

    # Columns
    id = Column("id_cliente",Integer,primary_key=True,)
    nome = Column("nome", String(200), nullable=False)
    cpf = Column("cpf", String(11), nullable=False, unique=True)
    email = Column("email", String(150), nullable=False, unique=True)
    telefone = Column("telefone", String(15), nullable=True)
    dados_publicos = Column("dados_publicos", Boolean, default=False)
    data_nascimento = Column("data_nascimento", Date)
    data_cadastro = Column("data_cadastro", DateTime, default=func.current_timestamp())