from flask import Flask
from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, Date, func
from flask_sqlalchemy import SQLAlchemy
from src.entities.base import Base


class Ambiente_Tempo(Base):
    __tablename__ = "ambiente_tempo"

    # Columns
    id = Column("id_ambiente_tempo",Integer,primary_key=True,)
    id_ambiente = Column("id_ambiente", Integer, nullable=False)
    oxigenio = Column("ar_oxigenio", Numeric(precision=7,scale=3), nullable=False)
    carbonico = Column("ar_carbonico", Numeric(precision=7,scale=3), nullable=False)
    poluentes = Column("ar_poluentes", Numeric(precision=7,scale=3), nullable=False)
    umidade = Column("ar_umidade", Numeric(precision=7,scale=3), nullable=False)
    densidade = Column("ar_densidade", Numeric(precision=7,scale=3), nullable=False)
    data_cadastro = Column("data_cadastro", DateTime, default=func.current_timestamp())