import mysql.connector
from manage import app
from flask import render_template, jsonify


def initialize_endpoints(api):
    #rota para a página inicial
    @app.route('/')
    def homepage():
        return render_template('homepage.html')

    @app.route('/blog')
    def blog():
        return 'Esse é o blog'

    

    @app.route('/cliente', methods = ['GET'])
    def get_clientes():
        con = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = 'trabalhopav'
        )
        try:
            cursor = con.cursor()
            try:
                cursor.execute("SELECT * FROM cliente;")
                clientes = cursor.fetchall()
            finally:
                cursor.close()
        finally:
            con.close()
        todos_clientes = [list(cliente) for cliente in clientes]
        return jsonify({"cliente": todos_clientes}),200


