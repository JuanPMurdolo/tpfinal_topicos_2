from flask.views import MethodView
from flask_smorest import abort, Blueprint
from flask_jwt_extended import jwt_required
from app.schemas import PredictSchema, PredictFinishedSchema
from app.models import PredictModel


from db import db
from sqlalchemy.exc import SQLAlchemyError

predictBlp = Blueprint(
    "predict", __name__, description="Operaciones de prediccion"
)

@predictBlp.route("/predict")
class Predict(MethodView):
    @jwt_required()
    @predictBlp.response(200, PredictFinishedSchema, many=True)
    def get(self):
        return PredictModel.query.all()
    
    @jwt_required()
    @predictBlp.arguments(PredictSchema)
    def post(self):
        prediction = PredictModel(**predictBlp.validated_args)
        db.session.add(prediction)
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
    
