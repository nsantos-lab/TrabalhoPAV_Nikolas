from flask import Flask
from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, Date, func
from flask_sqlalchemy import SQLAlchemy
from src.entities.base import Base


class Ambiente(Base):
    __tablename__ = "ambiente"

    # Columns
    id = Column("id_ambiente",Integer,primary_key=True,)
    cliente = Column("id_cliente", Integer, nullable=False)
    oxigenio = Column("ar_oxigenio", Numeric(precision=7,scale=3), nullable=False)
    carbonico = Column("ar_carbonico", Numeric(precision=7,scale=3), nullable=False)
    poluentes = Column("ar_poluentes", Numeric(precision=7,scale=3), nullable=False)
    umidade = Column("ar_umidade", Numeric(precision=7,scale=3), nullable=False)
    densidade = Column("ar_densidade", Numeric(precision=7,scale=3), nullable=False)
    dados_publicos = Column("dados_publicos", Boolean, default=False)
    data_cadastro = Column("data_cadastro", DateTime, default=func.current_timestamp())