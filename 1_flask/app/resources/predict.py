from flask.views import MethodView
from flask_smorest import abort, Blueprint
from flask_jwt_extended import jwt_required
from app.schemas import PredictSchema, PredictFinishedSchema
from app.models import PredictModel
from app.__init__ import modeloNeuronal
from flask_jwt_extended import get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from db import db
from sqlalchemy.exc import SQLAlchemyError

predictBlp = Blueprint(
    "predict", __name__, description="Operaciones de prediccion"
)

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["5 per minute"],
)

premium_limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["50 per minute"]
)

@predictBlp.route("/premium/predict")
class Predict(MethodView):
    @jwt_required()
    @limiter.limit("50 per minute")
    @predictBlp.response(200, PredictFinishedSchema, many=True)
    def get(self):
        if get_jwt_identity() != "premium":
            abort(403, message="No tienes permisos para acceder a esta ruta")
        else:
            return PredictModel.query.all()
    
    @jwt_required()
    @predictBlp.arguments(PredictSchema)
    @limiter.limit("50 per minute")
    def post(self):
        if get_jwt_identity() != "premium":
            abort(403, message="No tienes permisos para acceder a esta ruta")
        else:
            prediction = PredictModel(**predictBlp.validated_args)
            db.session.add(prediction)
            #en base al modelo neuronal, predecir el riesgo cardiaco, y agregarle el valor final a la instancia de la clase
            predictionComplete = modeloNeuronal.predict(prediction)
            if predictionComplete > 0.5:
                prediction.riesgoCardiaco = True
            else:
                prediction.riesgoCardiaco = False
            try:
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                abort(400, message=str(e.__dict__["orig"]))
            return {"message": "Predict"}
        
@predictBlp.route("/freemium/predict")
class Predict(MethodView):
    @jwt_required()
    @limiter.limit("5 per minute")
    @predictBlp.response(200, PredictFinishedSchema, many=True)
    def get(self):
        if get_jwt_identity() != "freemium":
            abort(403, message="No tienes permisos para acceder a esta ruta")
        else:
            return PredictModel.query.all()
    
    @jwt_required()
    @predictBlp.arguments(PredictSchema)
    @limiter.limit("5 per minute")
    def post(self):
        if get_jwt_identity() != "freemium":
            abort(403, message="No tienes permisos para acceder a esta ruta")
        else:
            prediction = PredictModel(**predictBlp.validated_args)
            db.session.add(prediction)
            #en base al modelo neuronal, predecir el riesgo cardiaco, y agregarle el valor final a la instancia de la clase
            predictionComplete = modeloNeuronal.predict(prediction)
            if predictionComplete > 0.5:
                prediction.riesgoCardiaco = True
            else:
                prediction.riesgoCardiaco = False
            try:
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                abort(400, message=str(e.__dict__["orig"]))
            return {"message": "Predict"}
    
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
    
