from flask import Flask,jsonify
import mysql.connector

app = Flask(__name__)

from routes.routes import *

if __name__ == '__main__':  #serve para so executar o app.py quando for o arquivo principal 
    app.run(debug=True)     #debug=True serve para atualizar o servidor automaticamente quando 
                            #houver alterações no código