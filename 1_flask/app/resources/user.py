from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity,  create_refresh_token
from schemas import UserRegisterSchema
from models.user import UserModel
from schemas import UserSchema
import os
import requests
from sqlalchemy import or_
from passlib.hash import pbkdf2_sha256 as sha256
from flask_pymongo import PyMongo
from sqlalchemy.exc import SQLAlchemyError


userBlp = Blueprint(
    "user", __name__, description="Operaciones de usuario"
)

@userBlp.route("/register")
class UserRegister(MethodView):
    @userBlp.arguments(UserRegisterSchema)
    @userBlp.response(201, UserRegisterSchema)
    def post(self, user_data):
        if UserModel.query.filter(
            or_(UserModel.username == user_data["username"],
                UserModel.email == user_data["email"])).first():
            abort(400, message="User already exists.")
        user = UserModel(
            username=user_data["username"],
            email = user_data["email"],
            password=sha256.hash(user_data["password"]),
            type = "freemium"
        )
        try:
            db.session.add(user)
            db.session.commit()
            #current_app.queue.enqueue(send_registration_email, user)

        except SQLAlchemyError:
            abort(500, message="Internal server error.")

        return {"message": "User created successfully."}

@userBlp.route("/login")
class UserLogin(MethodView):
    @userBlp.arguments(UserSchema)
    @userBlp.response(200, UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()
        if user and sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}
        else:
            abort(401, message="Invalid username or password.")

@userBlp.route("/SwitchToPremium")
class UserLogin(MethodView):
    @userBlp.arguments(UserSchema)
    @userBlp.response(200, UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()
        if user and sha256.verify(user_data["password"], user.password):
            user.type = "premium"
            db.session.commit()
            return {"message": "User is now premium"}
        else:
            abort(401, message="Invalid username or password.")