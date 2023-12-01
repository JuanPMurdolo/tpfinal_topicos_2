import os

from  flask import Flask, request 
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_smorest import Api, Blueprint, abort
from .db import db
import tensorflow as tf

from .resources.user import userBlp as UserBlueprint
from .resources.predict import PredictBlp as PredictBlueprint



def create_app(test_config=None):
    app = Flask(__name__)

    # cargar el modelo nueronal y despues usarlo 
    modeloNeuronal = tf.keras.models.load_model('../0_ai/model.keras')
    app.config["modeloNeuronal"] = modeloNeuronal

    app.config["API_TITLE"] = "Topicos 2 - TP FINAL"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_VERSION"] = "3.24.2"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app, db)

    app.config["JWT_SECRET_KEY"] = ""
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    api = Api(app)
    
    #blueprints
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(PredictBlueprint)
    
    
    return app