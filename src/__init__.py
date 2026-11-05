import os

from flask import Flask
from flask_restful import Api
from sqlalchemy.engine import URL
from src.routes.routes import initialize_endpoints, initialize_pages
from src.entities.base import db

# Função para criar a aplicação Flask
def create_app() -> Flask:
    # Cria a instância da aplicação Flask e define a configuração do banco de dados usando SQLAlchemy
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = URL.create(
        "mysql+pymysql",
        username=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "trabalhopav"),
    )

    db.init_app(app)
    initialize_pages(app)

    # Cria a instância da API Flask-RESTful e inicializa os endpoints
    api = Api(app, prefix="/trabalhopav")
    initialize_endpoints(api)

    return app