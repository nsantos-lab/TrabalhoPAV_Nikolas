from src.entities.ambiente import Ambiente
from src.entities.base import db
from src.exceptions import ResourceNotFoundError

def get_lista_ambientes():
    ambientes = db.session.query(Ambiente).all()
    return ambientes

def get_ambiente(ambiente_id):
    ambiente = db.session.query(Ambiente).get(ambiente_id)
    return ambiente

def add_ambiente(cliente_id: int, oxigenio: float, carbonico: float, poluentes: float, umidade: float, densidade: float, dados_publicos: bool):
    ambiente = Ambiente(cliente=cliente_id, oxigenio=oxigenio, carbonico=carbonico, poluentes=poluentes, umidade=umidade, densidade=densidade, dados_publicos=dados_publicos)
    # INSERT INTO Ambiente values (cliente, oxigenio, carbonico, poluentes, umidade, densidade, dados_publicos)
    db.session.add(ambiente)
    db.session.commit()
    return ambiente

def update_ambiente(id: int, cliente_id: int, oxigenio: float, carbonico: float, poluentes: float, umidade: float, densidade: float, dados_publicos: bool) -> Ambiente:
    ambiente = db.session.query(Ambiente).get(id)
    if(not ambiente):
        raise ResourceNotFoundError("Ambiente não encontrado.")

    ambiente.cliente = cliente_id
    ambiente.oxigenio = oxigenio
    ambiente.carbonico = carbonico
    ambiente.poluentes = poluentes
    ambiente.umidade = umidade
    ambiente.densidade = densidade
    ambiente.dados_publicos = dados_publicos

    db.session.commit()
    return ambiente

def delete_ambiente(ambiente_id):
    ambiente = db.session.query(Ambiente).get(ambiente_id)
    if not ambiente:
        raise ResourceNotFoundError("Ambiente não encontrado.")
    db.session.delete(ambiente)
    db.session.commit()
    return ambiente