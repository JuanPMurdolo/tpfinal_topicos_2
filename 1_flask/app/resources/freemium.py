from flask.views import MethodView
from flask_smorest import abort, Blueprint
from flask_jwt_extended import jwt_required
from ..schemas import PredictSchema, PredictFinishedSchema
from app.models import PredictModel, UserModel
from flask_jwt_extended import get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import current_app
import numpy as np
from ..db import db
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify


freemiumBlp = Blueprint(
    "predict", 'predict', url_prefix="freemium", description="Operaciones de prediccion"
)


def convertir_a_entrada_modelo(predict_data):
    # Suponiendo que predict_data es una instancia de PredictModel
    datos = [
        0,
        predict_data.colesterol,
        predict_data.presionArterial,
        predict_data.azucar,
        predict_data.edad,
        predict_data.sobrepeso,
        predict_data.tabaquismo,
    ]

    # Convertir a un formato adecuado para el modelo
    # Por ejemplo, puedes usar un arreglo NumPy
    datos_preprocesados = np.array(datos).reshape(1, -1)

    return datos_preprocesados

def usar_modelo_neuronal(predict_data): 
    modeloNeuronal = current_app.config["modeloNeuronal"]
    predict_data = convertir_a_entrada_modelo(predict_data)
    return float(modeloNeuronal.predict(predict_data))

@freemiumBlp.route("/predict")
class PredictFreemium(MethodView):
    @jwt_required(fresh=True)
    @freemiumBlp.response(200, PredictFinishedSchema(many=True))
    def get(self):
        current_user = get_jwt_identity()
        user = UserModel.query.filter_by(username=current_user).first()
        if user.type == "freemium":
            return PredictModel.query.all()
        else:
            abort(403, message="No tienes permisos para acceder a esta ruta")

    @jwt_required(fresh=True)
    @freemiumBlp.arguments(PredictSchema)
    @freemiumBlp.response(200, PredictFinishedSchema)
    def post(self, predict_data):
        current_user = get_jwt_identity()
        user = UserModel.query.filter_by(id=current_user).first()
        if user.type == "freemium":
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
        else:
            abort(403, message="No tienes permisos para acceder a esta ruta")
    
@freemiumBlp.route("/predictById/<string:predict_id>")
class PredictByIdFreemium(MethodView):
    @jwt_required(fresh=True)
    @freemiumBlp.response(200, PredictFinishedSchema)
    def get(self, predict_id: str):
        current_user = get_jwt_identity()
        user = UserModel.query.filter_by(username=current_user).first()
        if user.type == "freemium":
            return PredictModel.query.get_or_404(predict_id)
        else:
            abort(403, message="No tienes permisos para acceder a esta ruta")
