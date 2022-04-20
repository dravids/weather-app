from flask import request, make_response
from app import app, db, api_key, getResponseHeaders
from models.HttpResponse import HttpResponse
import requests, json
from models.analytics import analytics
from services import auth


@app.route('/auth/forecast/city', methods=['GET'])
@auth.token_required_by_role(["USER", "SUPERADMIN"])
def city_weather(current_user):
    """
    City weather function
    Gets executed on route /auth/forecast/city, supports only GET request for users/admin
    :param current_user: Used for analytics API
    :type times: Str
    """
    try:
        API_KEY = api_key
        payload: dict = request.json
        city: str = payload.get('city', None)
        days: int = payload.get('days', None)
        # Only checking condition for city since weather api by default assumes 1 day if day not specified"""   
        if city:
            url = f'http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days={days}&aqi=no&alerts=no'
            response = requests.get(url).json()
            status, message, response = auth.check_json(response)
            user_analytics = analytics(user_name=current_user, query=city)
            db.session.add(user_analytics)
            db.session.commit()
        else: 
            status, message, response = (400, 'Bad request: Parameter q is missing or malformed url', None)
        response = HttpResponse(message=message, status=status, data=response)
    except Exception as e:
        exception_str = str(e)
        response = HttpResponse(message='Exception Occured - ' + exception_str, status=500)

    return make_response(json.dumps(response.__dict__),response.status, getResponseHeaders())         




