from email import message
from flask import make_response, request
from app import app, db, api_key, getResponseHeaders
from models.HttpResponse import HttpResponse
from services import auth
import json
from models.Country import Country
from sqlalchemy import func



@app.route('/auth/countries', methods=['GET'])
@auth.token_required_by_role(["SUPERADMIN"])
def get_countries(current_user):
    country_list = []
    try:
        countries = db.session.query(Country.country).distinct()
        for country_obj in countries:
            country_list.append(country_obj.country)
        status = 200
        message = "Retrieved list of all coutries from database"
        response = HttpResponse(message=message, status=status, data={"countries": country_list})

    except Exception as e:
        exception_str = str(e)
        response = HttpResponse(message='Exception Occured - ' + exception_str, status=500)
    
    return make_response(json.dumps(response.__dict__),response.status, getResponseHeaders())  


@app.route('/auth/country/cities', methods=['GET'])
@auth.token_required_by_role(["SUPERADMIN"])
def get_cities_by_country(current_user):
    payload: dict = request.json
    country: str = payload.get('country', None)
    key = f'cities_in_{country}'
    cities_list = []
    try:
        cities = db.session.query(Country.city).filter(func.lower(Country.country) == func.lower(country)).distinct()
        for city_obj in cities:
            cities_list.append(city_obj.city)
        if len(cities_list)!= 0:
            status = 200
            message = f'Retrieved list of all cities in {country} from database'
        else:
            status = 404 #for no records found: server can not find the requested resource.
            message = f'No records found for {country}. Check the country name and try again'
        response = HttpResponse(message=message, status=status, data={str(key): cities_list})
    except Exception as e:
        exception_str = str(e)
        response = HttpResponse(message='Exception Occured - ' + exception_str, status=500)
    
    return make_response(json.dumps(response.__dict__),response.status, getResponseHeaders())  
