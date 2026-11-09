from src.entities.ambiente_tempo import Ambiente_Tempo
from src.entities.base import db
from src.exceptions import ResourceNotFoundError

def get_lista_ambiente_tempos():
    ambiente_tempos = db.session.query(Ambiente_Tempo).all()
    return ambiente_tempos

def get_ambiente_tempo(ambiente_tempo_id):
    ambiente_tempo = db.session.query(Ambiente_Tempo).get(ambiente_tempo_id)
    return ambiente_tempo

def add_ambiente_tempo(ambiente_id: int, oxigenio: float, carbonico: float, poluentes: float, umidade: float, temperatura: float):
    ambiente_tempo = Ambiente_Tempo(id_ambiente=ambiente_id, oxigenio=oxigenio, carbonico=carbonico, poluentes=poluentes, umidade=umidade, temperatura=temperatura)
    # INSERT INTO Ambiente_Tempo values (ambiente, oxigenio, carbonico, poluentes, umidade, temperatura)
    db.session.add(ambiente_tempo)
    db.session.commit()
    return ambiente_tempo

def update_ambiente_tempo(id: int, ambiente_id: int, oxigenio: float, carbonico: float, poluentes: float, umidade: float, temperatura: float) -> Ambiente_Tempo:
    ambiente_tempo = db.session.query(Ambiente_Tempo).get(id)
    if(not ambiente_tempo):
        raise ResourceNotFoundError("Tempo de ambiente não encontrado.")

    ambiente_tempo.id_ambiente = ambiente_id
    ambiente_tempo.oxigenio = oxigenio
    ambiente_tempo.carbonico = carbonico
    ambiente_tempo.poluentes = poluentes
    ambiente_tempo.umidade = umidade
    ambiente_tempo.temperatura = temperatura

    db.session.commit()
    return ambiente_tempo

def delete_ambiente_tempo(ambiente_tempo_id):
    ambiente_tempo = db.session.query(Ambiente_Tempo).get(ambiente_tempo_id)
    if not ambiente_tempo:
        raise ResourceNotFoundError("Tempo de ambiente não encontrado.")
    db.session.delete(ambiente_tempo)
    db.session.commit()
    return ambiente_tempo