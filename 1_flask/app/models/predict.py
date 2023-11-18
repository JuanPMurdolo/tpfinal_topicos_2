from db import db

class PredictModel(db.Model):
    __tablename__ = "predict"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))
    presionArterial = db.Column(db.Float)
    colesterol = db.Column(db.Float)
    azucar = db.Column(db.Float)
    masaCorporal = db.Column(db.Float)
    edad = db.Column(db.Integer)
    riesgoCardiaco = db.Column(db.Boolean)