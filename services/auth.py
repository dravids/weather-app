from flask import request, make_response
from app import app, db, secret_key
from models.HttpResponse import HttpResponse
import jwt
from functools import wraps
from models.User import User


def token_required_by_role(roles: list):
    """
    Token Decorator with decorator param
    Used to pass a list of roles to authorize resources
    :param roles: List of roles ["SUPERADMIN", "ADMIN", "USER"]
    :type roles: List class
    """
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization']
                if token and len(token.split(" ")) == 2:
                    token = token.split(" ")[1]
                else:
                    return make_response({'message' : 'Please specify token as Bearer <token> in Authorization Header'}), 400

            if not token:
                return make_response({'message' : 'JWT Token is missing !!'}), 401
    
            try:
                data = jwt.decode(token, key=secret_key, algorithms=["HS256"])
                current_user = User.query\
                    .filter(User.user_name == data['user_name'])\
                    .first()
                current_user_roles = [role for role in data["roles"]]
                if set(roles).isdisjoint(set(current_user_roles)):
                    return make_response({
                    'message' : f'Forbidden'
                }), 403

            except Exception as e:
                return make_response({
                    'message' : f'Error occured while authenticating user : {e}'
                }), 401
            return  f(current_user.user_name, *args, **kwargs)
    
        return decorated
    return token_required


def check_json(json_data):
    if json_data.get("location"):
        status, message, response = (200, 'Successfully fetched api response', json_data)
    else: 
        #404 is not the right response, but giving it for catching it later since some places/random strings in query might not exist
        status, message, response = (404, 'Location not available', json_data.get("error"))
    return status, message, response