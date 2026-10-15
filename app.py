from flask import Flask

app = Flask(__name__)

from scr.routes.routes import *

if __name__ == '__main__':  #serve para so executar o app.py quando for o arquivo principal 
    app.run()

