import os

from  flask import Flask
from flask_jwt_extended import JWTManager
from .db import db
import tensorflow as tf


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # cargar el modelo nueronal y despues usarlo 
    modeloNeuronal = tf.keras.models.load_model('../0_ai/model.keras')

    app.config["API_TITLE"] = "Topicos 2 - TP FINAL"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_JSON_PATH"] = "api-spec.json"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/"
    app.config["OPENAPI_SWAGGER_UI_VERSION"] = "3.24.2"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/"
    app.config["OPENAPI_SWAGGER_UI_CONFIGURATION"] = {
        "displayOperationId": True
    }
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    app.config["JWT_SECRET_KEY"] = ""
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    #blueprints
    
    return app