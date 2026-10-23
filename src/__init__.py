from flask import Flask
from flask_restful import Api
from src.routes.routes import initialize_endpoints, initialize_pages
from src.entities.base import db

# Função que cria a API
def create_app() -> Flask:
    # Definindo qual é o banco de dados
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/trabalhopav'

    db.init_app(app)
    initialize_pages(app)

    # Flask API - Controllers/Endpoints - URL
    api = Api(app, prefix="/trabalhopav")
    initialize_endpoints(api)

    return app