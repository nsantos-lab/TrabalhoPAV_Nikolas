from src.repositories.AmbienteRepository import get_lista_ambientes, get_ambiente, add_ambiente, update_ambiente, delete_ambiente
from src.entities.ambiente import Ambiente
from marshmallow import ValidationError
from math import isfinite

# Implementação das regras de negócio no cadastro do cliente. CRUD

def getAmbientes():
    return get_lista_ambientes()

def getAmbiente(ambiente_id):
    return get_ambiente(ambiente_id)

def _validar_ambiente(cliente_id, oxigenio, carbonico, poluentes, umidade, densidade, dados_publicos):
    if cliente_id is None or cliente_id < 0:
        raise ValidationError({"cliente": "Cliente ID must not be null or negative."})
    for field, value in {
        "oxigenio": oxigenio,
        "carbonico": carbonico,
        "poluentes": poluentes,
        "umidade": umidade,
        "densidade": densidade,
    }.items():
        if value is None or not isfinite(value) or value < 0:
            raise ValidationError({field: f"{field.capitalize()} must be a finite, non-negative number."})
    if dados_publicos is None:
        raise ValidationError({"dados_publicos": "Dados públicos must not be null."})

def addAmbiente(cliente_id: int, oxigenio: float, carbonico: float, poluentes: float, umidade: float, densidade: float, dados_publicos: bool) -> Ambiente:
    _validar_ambiente(cliente_id, oxigenio, carbonico, poluentes, umidade, densidade, dados_publicos)

    return add_ambiente(cliente_id, oxigenio, carbonico, poluentes, umidade, densidade, dados_publicos)

def updateAmbiente(id: int, cliente_id: int, oxigenio: float, carbonico: float, poluentes: float, umidade: float, densidade: float, dados_publicos: bool):
    _validar_ambiente(cliente_id, oxigenio, carbonico, poluentes, umidade, densidade, dados_publicos)
    return update_ambiente(id=id, cliente_id=cliente_id, oxigenio=oxigenio, carbonico=carbonico, poluentes=poluentes, umidade=umidade, densidade=densidade, dados_publicos=dados_publicos)

def deleteAmbiente(ambiente_id):
    return delete_ambiente(ambiente_id)
