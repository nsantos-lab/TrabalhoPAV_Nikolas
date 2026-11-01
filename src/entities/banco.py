from flask import Flask
from sqlalchemy import Column, Integer, Numeric, String
from flask_sqlalchemy import SQLAlchemy
from src.entities.base import Base


class Banco(Base):
    __tablename__ = "banco"

    # Columns
    id_banco = Column("id_banco",Integer,primary_key=True,)
    id_cliente = Column("id_cliente", Integer, nullable=False, unique=True)
    dinheiro = Column("dinheiro", Numeric(precision=10,scale=3), nullable=False)
    senha = Column("senha", String(100), nullable=False)