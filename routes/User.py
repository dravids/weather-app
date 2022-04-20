from flask import request, make_response
from app import app, db, secret_key, getResponseHeaders
from models.HttpResponse import HttpResponse
import json
from models.UserSessions import UserSession
from services import auth
from services import User as user_service
import jwt
import datetime
from functools import wraps
from models.User import User

@app.route('/login', methods=['POST'])
def login():
    try:
        payload: dict = request.json
        user_name: str = payload.get('user_name', None)
        password: str = payload.get('password', None)

        if user_name and password:
            status, message, data = user_service.validate_user_credentials(user_name=user_name, password=password)
            if status == 200:
                access_token = jwt.encode(payload=data, key=secret_key, algorithm="HS256")
                ## writing to sessions table
                expires_at = data["exp"]
                issued_at = data["iat"]
                user_session = UserSession(user_name=data['user_name'], token=access_token, status="active", inserted_at=issued_at, updated_at=expires_at, expires_at=expires_at)
                db.session.add(user_session)
                db.session.commit()
                data['access_token'] = access_token

        else:
            status, message, data = (400, 'Bad request', None)

        response = HttpResponse(message=message, status=status, data=data)

    except Exception as e:
        exception_str = str(e)
        response = HttpResponse(message='Exception Occured - ' + exception_str, status=500)

    return make_response(json.dumps(response.__dict__, default=str), response.status, getResponseHeaders())
    

@app.route('/logout', methods=['POST'])
@auth.token_required_by_role(["SUPERADMIN", "USER"])
def logout_user(current_user):
    try:
        db.session.query(UserSession).filter(UserSession.user_name == current_user).update({'status': 'inactive', 'updated_at': datetime.datetime.utcnow()})
        db.session.commit()
        message="Logged out successfully"
        status=200
        data={"User": current_user}
        response = HttpResponse(message=message, status=status, data=data)
    except Exception as e:
        exception_str = str(e)
        response = HttpResponse(message='Exception Occured - ' + exception_str, status=500)
    return make_response(json.dumps(response.__dict__),response.status, getResponseHeaders())  




@app.route('/register', methods=['POST'])
def register():
        payload: dict = request.json
        first_name: str = payload.get('first_name', None)
        last_name: str = payload.get('last_name', None)
        user_email: str = payload.get('user_email', None)
        user_name: str = payload.get('user_name', None)
        password: str = payload.get('password', None)

        try:
            if user_name and password and user_email and first_name and last_name:
                print ("Valid input")
                status, message, data = user_service.check_and_add_user_details(user_name=user_name, 
                                                                                user_email=user_email, 
                                                                                password=password,
                                                                                first_name=first_name,
                                                                                last_name=last_name)

            else:
                status, message, data = (400, 'Bad request', None)

            response = HttpResponse(message=message, status=status, data=data)

        except Exception as e:
            exception_str = str(e)
            response = HttpResponse(message='Exception Occured - ' + exception_str, status=500)

        return make_response(json.dumps(response.__dict__),response.status, getResponseHeaders())


#test api for JWT 
@app.route('/auth/users', methods =['GET'])
@auth.token_required_by_role(["SUPERADMIN"])
def get_all_users(current_user):
    """querying the database using return_all class method for all the entries in it"""
    try:
        users = User.return_all()
        status = 200
        message = "Successfully fetched all the users"
        response = HttpResponse(message=message, status=status, data=users)
    except Exception as e:
        exception_str = str(e)
        response = HttpResponse(message='Exception Occured - ' + exception_str, status=500)

    return make_response(json.dumps(response.__dict__),response.status, getResponseHeaders())         



       




