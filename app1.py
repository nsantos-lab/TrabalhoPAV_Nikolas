from flask import Flask,jsonify
import mysql.connector

app = Flask(__name__)

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

from routes.routes import *

if __name__ == '__main__':  #serve para so executar o app.py quando for o arquivo principal 
    app.run(debug=True)  #debug=True serve para atualizar o servidor automaticamente quando houver alterações no código

