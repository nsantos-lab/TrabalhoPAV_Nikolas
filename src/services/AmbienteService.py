from src.repositories.AmbienteRepository import get_lista_ambientes, get_ambiente, add_ambiente, update_ambiente, delete_ambiente
from src.entities.ambiente import Ambiente
from marshmallow import ValidationError
from datetime import date

# Implementação das regras de negócio no cadastro do cliente. CRUD

def getAmbientes():
    return get_lista_ambientes()

def getAmbiente(ambiente_id):
    return get_ambiente(ambiente_id)

def addAmbiente(cliente_id: int, oxigenio: float, carbonico: float, poluentes: float, umidade: float, densidade: float, dados_publicos: bool) -> Ambiente:
    if(cliente_id is None):
        raise ValidationError("Cliente ID must not be null.")
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

    return add_ambiente(cliente_id, oxigenio, carbonico, poluentes, umidade, densidade, dados_publicos)

def updateAmbiente(id: int, cliente_id: int, oxigenio: float, carbonico: float, poluentes: float, umidade: float, densidade: float, dados_publicos: bool):
    return update_ambiente(id=id, cliente_id=cliente_id, oxigenio=oxigenio, carbonico=carbonico, poluentes=poluentes, umidade=umidade, densidade=densidade, dados_publicos=dados_publicos)

def deleteAmbiente(ambiente_id):
    return delete_ambiente(ambiente_id)
