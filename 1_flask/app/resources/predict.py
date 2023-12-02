from flask.views import MethodView
from flask_smorest import abort, Blueprint
from flask_jwt_extended import jwt_required
from ..schemas import PredictSchema, PredictFinishedSchema
from app.models import PredictModel
from flask_jwt_extended import get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import current_app
import numpy as np
from ..db import db
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify

predictBlp = Blueprint(
    "predict", 'predict', description="Operaciones de prediccion"
)

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["5 per minute"],
)

premium_limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["50 per minute"]
)

def convertir_a_entrada_modelo(predict_data):
    # Suponiendo que predict_data es una instancia de PredictModel
    datos = [
        predict_data.presionArterial,
        predict_data.colesterol,
        predict_data.azucar,
        predict_data.masaCorporal,
        predict_data.edad,
        predict_data.sobrepeso,
        predict_data.tabaquismo
    ]

    # Convertir a un formato adecuado para el modelo
    # Por ejemplo, puedes usar un arreglo NumPy
    datos_preprocesados = np.array(datos).reshape(1, -1)

    return datos_preprocesados

def usar_modelo_neuronal(predict_data): 
    modeloNeuronal = current_app.config["modeloNeuronal"]
    predict_data = convertir_a_entrada_modelo(predict_data)
    return float(modeloNeuronal.predict(predict_data))
    

@predictBlp.route("/premium/predict")
class Predict(MethodView):
    @jwt_required(fresh=True)
    @limiter.limit("50 per minute")
    @predictBlp.response(200, PredictFinishedSchema)
    def get(self):
        if get_jwt_identity() != "premium":
            abort(403, message="No tienes permisos para acceder a esta ruta")
        else:
            return PredictModel.query.all()
    
    @jwt_required(fresh=True)
    @predictBlp.arguments(PredictSchema)
    @limiter.limit("50 per minute")
    def post(self, predict_data):
        if get_jwt_identity() != "premium":
            abort(403, message="No tienes permisos para acceder a esta ruta")
        else:
            prediction = PredictModel(**predict_data)
            #en base al modelo neuronal, predecir el riesgo cardiaco, y agregarle el valor final a la instancia de la clase
            predictionComplete = usar_modelo_neuronal(prediction)
            if predictionComplete > 0.5:
                prediction.riesgoCardiaco = True
            else:
                prediction.riesgoCardiaco = False
            try:
                db.session.add(prediction)
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                abort(400, message="Error en la bbdd")
            return prediction
        
@predictBlp.route("/freemium/predict")
class Predict(MethodView):
    #@jwt_required(fresh=True)
    @limiter.limit("5 per minute")
    @predictBlp.response(200, PredictFinishedSchema(many=True))
    def get(self):
        #print(get_jwt_identity())
        #if get_jwt_identity() != "freemium":
            #abort(403, message="No tienes permisos para acceder a esta ruta")
        #else:
            return PredictModel.query.all()
    
    #@jwt_required(fresh=True)
    @predictBlp.arguments(PredictSchema)
    @limiter.limit("5 per minute")
    def post(self, predict_data):
        #if get_jwt_identity() != "freemium":
        #    abort(403, message="No tienes permisos para acceder a esta ruta")
        #else:
            prediction = PredictModel(**predict_data)
            #db.session.add(prediction)
            #en base al modelo neuronal, predecir el riesgo cardiaco, y agregarle el valor final a la instancia de la clase
            predictionComplete = usar_modelo_neuronal(prediction)
            if predictionComplete > 0.5:
                prediction.riesgoCardiaco = True
            else:
                prediction.riesgoCardiaco = False
            
            try:
                db.session.add(prediction)
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                abort(400, message="Error en la bbdd")
            return prediction
    
@predictBlp.route("/predict/<string:predict_id>")
class PredictById(MethodView):
    @jwt_required()
    def get(self, predict_id: str):
        return {"message": "PredictById"}
    
    @jwt_required()
    def delete(self, predict_id: str):
        return {"message": "PredictById"}
    
    @jwt_required()
    def put(self, predict_id: str):
        return {"message": "PredictById"}
    
