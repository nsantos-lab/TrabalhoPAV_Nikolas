from src.repositories.Ambiente_TempoRepository import get_lista_ambiente_tempos, get_ambiente_tempo, add_ambiente_tempo, update_ambiente_tempo, delete_ambiente_tempo
from src.entities.ambiente_tempo import Ambiente_Tempo
from marshmallow import ValidationError
from datetime import date

# Implementação das regras de negócio no cadastro do cliente. CRUD

def getAmbiente_Tempos():
    return get_lista_ambiente_tempos()

def getAmbiente_Tempo(ambiente_tempo_id):
    return get_ambiente_tempo(ambiente_tempo_id)

def addAmbiente_Tempo(ambiente_id: int, oxigenio: float, carbonico: float, poluentes: float, umidade: float, densidade: float) -> Ambiente_Tempo:
    if(ambiente_id is None):
        raise ValidationError("Ambiente ID must not be null.")
    if(oxigenio is None or oxigenio < 0):
        raise ValidationError("Oxigenio must not be null or negative.")
    if(carbonico is None or carbonico < 0):
        raise ValidationError("Carbonico must not be null or negative.")
    if(poluentes is None or poluentes < 0):
        raise ValidationError("Poluentes must not be null or negative.")
    if(umidade is None or umidade < 0):
        raise ValidationError("Umidade must not be null or negative.")
    if(densidade is None or densidade < 0):
        raise ValidationError("Densidade must not be null or negative.")

    return add_ambiente_tempo(ambiente_id, oxigenio, carbonico, poluentes, umidade, densidade)

def updateAmbiente_Tempo(id: int, ambiente_id: int, oxigenio: float, carbonico: float, poluentes: float, umidade: float, densidade: float):
    return update_ambiente_tempo(id=id, ambiente_id=ambiente_id, oxigenio=oxigenio, carbonico=carbonico, poluentes=poluentes, umidade=umidade, densidade=densidade)

def deleteAmbiente_Tempo(ambiente_tempo_id):
    return delete_ambiente_tempo(ambiente_tempo_id)
