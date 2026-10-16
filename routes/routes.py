import mysql.connector
from app import app
from flask import render_template, jsonify

#rota para a página inicial
@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/blog')
def blog():
    return 'Esse é o blog'

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
    return jsonify({"tables": table_names}),200  # jsonify converte uma lista em python para um objeto JSON, 
                                                 # que é o formato de dados usado em APIs RESTful