from marshmallow import Schema, fields, validate

class PredictSchema(Schema):
    id = fields.Str(dump_only=True)
    nombre = fields.Str(default="Natalia Natalia", validate=validate.Length(min=1))
    presionArterial = fields.Float(required=True)
    colesterol = fields.Float(required=True)
    azucar = fields.Float(required=True)
    masaCorporal = fields.Float(required=True)
    edad = fields.Int(required=True)
    sobrepeso = fields.Boolean(required=True)
    tabaquismo = fields.Boolean(required=True)

class PredictFinishedSchema(PredictSchema):
    riesgoCardiaco = fields.Boolean(required=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    type = fields.Str(required=True)

class UserRegisterSchema(UserSchema):
    email = fields.Email(required=True)