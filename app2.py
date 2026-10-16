from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

con = mysql.connector.connect(  # gera a conexao com o banco
    host = 'localhost',
    user = 'root',
    password = 'root',
    database = 'trabalhopav'
)

@app.route('/tables', methods = ['GET'])
def get_tables():
    cursor = con.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    cursor.close()
    con.close()
    table_names = [table[0] for table in tables]
    return jsonify({"tables": table_names}),200  # jsonify converte uma lista em python para um objeto JSON, 
                                                 # que é o formato de dados usado em APIs RESTful
