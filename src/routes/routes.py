from src.controllers.ClienteController import ClienteList, ClienteItem

def initialize_endpoints(api):

    # Especifico a classe do Controller responsável por essa rota: AlunoList
    # Especifico a rota: /alunos
    api.add_resource(ClienteList, "/clientes")
    api.add_resource(ClienteItem, "/clientes/<int:cliente_id>")
