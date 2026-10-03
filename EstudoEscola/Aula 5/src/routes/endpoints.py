from src.controllers.AlunoController import AlunoList, AlunoItem

def initialize_endpoints(api):

    # Especifico a classe do Controller responsável por essa rota: AlunoList
    # Especifico a rota: /alunos
    api.add_resource(AlunoList, "/alunos")
    api.add_resource(AlunoItem, "/alunos/<int:aluno_id>")
