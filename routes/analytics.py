from flask import make_response, request
from app import app, db, api_key, getResponseHeaders
from models.HttpResponse import HttpResponse
from models.analytics import analytics
from services import auth
import json
from models.UserSessions import UserSession
from sqlalchemy import func



@app.route('/auth/analytics/online/users', methods=['GET'])
@auth.token_required_by_role(["SUPERADMIN"])
def get_active_users(current_user):
    user_list = []
    try:
        active_users = db.session.query(UserSession.user_name).filter(UserSession.status == "active").distinct()
        for user in active_users:
            user_list.append(user.user_name)
        status = 200
        message = "Retrieved list of all active users from database"
        response = HttpResponse(message=message, status=status, data={"users": user_list})

    except Exception as e:
        exception_str = str(e)
        response = HttpResponse(message='Exception Occured - ' + exception_str, status=500)
    
    return make_response(json.dumps(response.__dict__),response.status, getResponseHeaders())


@app.route('/auth/analytics/users', methods=['GET'])
@auth.token_required_by_role(["SUPERADMIN"])
def get_top_n_users(current_user): 
    payload: dict = request.json
    n: str = payload.get('n', None)
    user_list = []
    try:
        users = db.session.query(analytics.user_name, func.count(analytics.query)).group_by(analytics.user_name).order_by(func.count(analytics.query).desc()).limit(n).all()

        for user in users:
            user_list.append({user[0]: user[1]})
        if len(user_list)!= 0:
            status = 200
            message = f'Retrieved top {n} users from database'
        else:
            status = 404 #for no records found: server can not find the requested resource.
            message = 'No records found'
        response = HttpResponse(message=message, status=status, data={"users": user_list})
    except Exception as e:
        exception_str = str(e)
        response = HttpResponse(message='Exception Occured - ' + exception_str, status=500)
    
    return make_response(json.dumps(response.__dict__),response.status, getResponseHeaders()) 



@app.route('/auth/analytics/queries', methods=['GET'])
@auth.token_required_by_role(["SUPERADMIN"])
def get_top_n_queries(current_user): 
    payload: dict = request.json
    n: str = payload.get('n', None)
    query_list = []
    try:
        queries = db.session.query(analytics.query, func.count(analytics.query)).group_by(func.lower(analytics.query)).order_by(func.count(analytics.query).desc()).limit(n).all()
        for query in queries:
            query_list.append({query[0]: query[1]})
        if len(query_list)!= 0:
            status = 200
            message = f'Retrieved top {n} queries from database'
        else:
            status = 404 #for no records found: server can not find the requested resource.
            message = 'No records found'
        response = HttpResponse(message=message, status=status, data={"queries": query_list})
    except Exception as e:
        exception_str = str(e)
        response = HttpResponse(message='Exception Occured - ' + exception_str, status=500)
    
    return make_response(json.dumps(response.__dict__),response.status, getResponseHeaders()) 