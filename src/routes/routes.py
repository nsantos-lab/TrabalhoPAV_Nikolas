from flask import Flask, jsonify, render_template
import mysql.connector
from src.controllers.ClienteController import ClienteList, ClienteItem
from src.controllers.AmbienteController import AmbienteList, AmbienteItem
from src.controllers.Ambiente_TempoController import Ambiente_TempoList, Ambiente_TempoItem

def initialize_pages(app: Flask) -> None:
    @app.get("/homepage")
    def homepage():
        return render_template("homepage.html")
    
    @app.get("/trabalhopav")
    def trabalhopav():
        return render_template("homepage.html")
    
    @app.route('/tables', methods = ['GET'])
    def get_tables():
        con = mysql.connector.connect(  # gera a conexao com o banco
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = 'trabalhopav'
        )
        try:
            cursor = con.cursor()
            try:
                cursor.execute("SHOW TABLES;")
                tables = cursor.fetchall()
            finally:
                cursor.close()
        finally:
            con.close()
        table_names = [table[0] for table in tables]
        return jsonify({"tables": table_names}),200 # jsonify converte uma lista em python para um objeto JSON, 
                                                    # que é o formato de dados usado em APIs RESTful

def initialize_endpoints(api):
    # Especifico a classe do Controller responsável por essa rota: AlunoList
    # Especifico a rota: /alunos
    api.add_resource(ClienteList, "/clientes")
    api.add_resource(ClienteItem, "/clientes/<int:cliente_id>")
    api.add_resource(AmbienteList, "/ambientes")
    api.add_resource(AmbienteItem, "/ambientes/<int:ambiente_id>")
    api.add_resource(Ambiente_TempoList, "/ambientes_tempo")
    api.add_resource(Ambiente_TempoItem, "/ambientes_tempo/<int:ambiente_tempo_id>")
