from src.repositories.Ambiente_TempoRepository import get_lista_ambiente_tempos, get_ambiente_tempo, add_ambiente_tempo, update_ambiente_tempo, delete_ambiente_tempo
from src.entities.ambiente_tempo import Ambiente_Tempo
from marshmallow import ValidationError
from math import isfinite

# Implementação das regras de negócio no cadastro do cliente. CRUD

def getAmbiente_Tempos():
    return get_lista_ambiente_tempos()

def getAmbiente_Tempo(ambiente_tempo_id):
    return get_ambiente_tempo(ambiente_tempo_id)

def _validar_ambiente_tempo(ambiente_id, oxigenio, carbonico, poluentes, umidade, temperatura):
    if ambiente_id is None or ambiente_id < 0:
        raise ValidationError({"ambiente": "Ambiente ID must not be null or negative."})
    for field, value in {
        "oxigenio": oxigenio,
        "carbonico": carbonico,
        "poluentes": poluentes,
        "umidade": umidade,
    }.items():
        if value is None or not isfinite(value) or value < 0:
            raise ValidationError({field: f"{field.capitalize()} must be a finite, non-negative number."})
    if temperatura is None:
        raise ValidationError({"temperatura": "Temperatura must not be null."})
    if temperatura > 200.0 or temperatura < -273.15:
        raise ValidationError({"temperatura": "Temperatura must not be lower than -273.15 or higher than 200.0."})

def addAmbiente_Tempo(ambiente_id: int, oxigenio: float, carbonico: float, poluentes: float, umidade: float, temperatura: float) -> Ambiente_Tempo:
    _validar_ambiente_tempo(ambiente_id, oxigenio, carbonico, poluentes, umidade, temperatura)

    return add_ambiente_tempo(ambiente_id, oxigenio, carbonico, poluentes, umidade, temperatura)

def updateAmbiente_Tempo(id: int, ambiente_id: int, oxigenio: float, carbonico: float, poluentes: float, umidade: float, temperatura: float):
    _validar_ambiente_tempo(ambiente_id, oxigenio, carbonico, poluentes, umidade, temperatura)
    return update_ambiente_tempo(id=id, ambiente_id=ambiente_id, oxigenio=oxigenio, carbonico=carbonico, poluentes=poluentes, umidade=umidade, temperatura=temperatura)

def deleteAmbiente_Tempo(ambiente_tempo_id):
    return delete_ambiente_tempo(ambiente_tempo_id)
