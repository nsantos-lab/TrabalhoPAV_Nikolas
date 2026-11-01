from flask import Flask
from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, Date, func
from flask_sqlalchemy import SQLAlchemy
from src.entities.base import Base


class Produto(Base):
    __tablename__ = "produto"

    # Columns
    id = Column("id_produto",Integer,primary_key=True,)
    id_ambiente = Column("id_ambiente", Integer, nullable=False)
    tipo = Column("tipo", String(20), nullable=False)
    preco = Column("preco", Numeric(precision=7,scale=3), nullable=False)
    potencia = Column("potencia", Numeric(precision=7,scale=3), nullable=False)
    