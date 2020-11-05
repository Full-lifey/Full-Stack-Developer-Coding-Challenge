from flask_jwt_extended import create_access_token
from sqlalchemy import inspect
from flask_restful import Resource
from flask import request

from models import db, UserModel

class Signup(Resource):
    def post(self):
        if request.is_json:
            email = request.json["email"]
            password = request.json["password"]
        else:
            email = request.form["email"]
            password = request.form["password"]
        # Check if user exists
        user_test = UserModel.query.filter_by(email=email).first()
        if user_test:
            return {"message":"User Already Exists"}, 409
        else :
            user = UserModel(email=email)
            user.set_password(password)
            db.session.add(user)
            try:
                db.session.commit()
                access_token = create_access_token(identity=email)
                return {"message":"Account Successfully Created", "access_token":access_token}, 201
            except:
                db.session.rollback()
                return {"message":"Internal Server Error"}, 500


class Login(Resource):
    def post(self):
        if request.is_json:
            email = request.json["email"]
            password = request.json["password"]
        else:
            email = request.form["email"]
            password = request.form["password"]
        # Find User Record
        user = UserModel.query.filter_by(email=email).first()
        if user:
            if user.check_password(password):
                access_token = create_access_token(identity=email)
                return {"message":"Login Success", "access_token":access_token}, 201
            else:
                return {"message":"Email or Password Incorrect"}, 401
        else:
            return {"message": "No user found with requested email"}, 401
