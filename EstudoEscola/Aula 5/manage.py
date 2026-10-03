# Criação de packages/pacotes dentro de uma API:
# src: Contém os arquivos relacionados ao código da API 
# entities/models: Contém as classes que correspondem as tabelas do banco de dados;
# ex: Tabela Aluno(id, nome, cpf, usuarioId, dtCadastro) então classe Aluno(id, nome, cpf)
# repositories/persistence: Contém as classes responsáveis por realizar as operações no 
# Banco de dados: Save, Update, Delete, Select. Cada entity possui um repository.
# Ex: classe AlunoRepository
# services: Contém as classes que são responsáveis por implementar as 
# regras de negócio da API/Requisitos. Cada entity pode possuir um service associado.
# Ex: classe AlunoService. validação de nome e cpf.
# controllers: Contém classes que implementam os métodos que recebem 
# as requisições HTTP (GET, POST, PUT, PATCH, DELETE) para um determinado objeto.
# Ex: AlunoController. 
# routes: Contém as rotas (URL) que a API sabe responder/tratar.
# dtos/view: Contém as classes que mapeiam os objetos que são recebidos pelos controllers.
# Ex: AlunoDTO. Especifica somente os atributos que são visíveis para
# o usuário: nome, cpf

# API: É um serviço e precisa de um host e uma porta.
# Ex: flask --app manage run --host=0.0.0.0 --port=8080
# Se não especificar a porta a API irá tentar subir na porta padrão do flask: 5000

from src import create_app

app = create_app()

