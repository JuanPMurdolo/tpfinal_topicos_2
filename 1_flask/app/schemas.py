from marshmallow import Schema, fields, validate

class PredictSchema(Schema):
    id = fields.Str(dump_only=True)
    nombre = fields.Str(default="Natalia Natalia", validate=validate.Length(min=1))
    presionArterial = fields.Float(required=True)
    colesterol = fields.Float(required=True)
    azucar = fields.Float(required=True)
    masaCorporal = fields.Float(required=True)
    edad = fields.Int(required=True)
    
class PredictFinishedSchema(PredictSchema):
    riesgoCardiaco = fields.Boolean(required=True)
