from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required, current_user

from .util.dto import UserDTO
from .util.jwt import unset_jwt
from service.auth_service import *

api = UserDTO.api
_user = UserDTO.user


@api.route('/user')
class User(Resource):
    @api.doc('Get current user info')
    @api.marshal_with(_user, mask='userid,username,company')
    @jwt_required()
    def get(self):
        resp = current_user
        return resp

    @api.doc('Register new user')
    @api.response(201, 'Created')
    @api.response(400, 'Bad Request')
    @api.response(409, 'Resource already exists')
    @api.expect(_user, validate=True)
    def post(self):
        data = request.get_json()
        try:
            resp = create_user(data)
            return resp
        except Exception as e:
            api.abort(500, reason=e)


@api.route('/login')
class Login(Resource):
    @api.doc('Login')
    @api.response(200, 'OK')
    @api.response(400, 'Bad Request')
    def post(self):
        data = request.get_json()
        return login_user(data)


@api.route('/logout')
class Logout(Resource):
    @api.doc('Logout')
    @api.response(200, 'OK')
    def get(self):
        resp = {
            'msg': 'Logout successful.'
        }
        return unset_jwt(resp)