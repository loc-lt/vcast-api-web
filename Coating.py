from os import access
from constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
from flask import Blueprint, app, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flasgger import swag_from
from database import *
from ERROR import *
import datetime
from threading import Thread

Coating = Blueprint("Coating", __name__, url_prefix="/api/v1/Casting")

@Coating.post('/InsertTempHuid')
@swag_from('./docs/Coating/DataTemp_Coating.yaml')
def Insert_Temp():
    try:
        Time_get = request.json['Time_get']
        Temperature1 = request.json['Temperature1']
        Humidity1 = request.json['Humidity1']
        Temperature2 = request.json['Temperature2']
        Humidity2 = request.json['Humidity2']
        Temperature3 = request.json['Temperature3']
        Humidity3 = request.json['Humidity3']
        Temperature4 = request.json['Temperature4']
        Humidity4= request.json['Humidity4']
        Temperature5 = request.json['Temperature5']
        Humidity5 = request.json['Humidity5']
        average_temp1 = request.json['average_temp1']
        average_humid1 = request.json['average_humid1']
        Coating = request.json['Coating']
        print("INSERT INTO [Coating].[dbo].["+Coating+"](Time_get,Temperature1,Humidity1,Temperature2,Humidity2,Temperature3,Humidity3,Temperature4,Humidity4,Temperature5,Humidity5,average_temp1,average_humid1) "
                        "VALUES ('"+Time_get+"','"+Temperature1+"', '"+Humidity1+"', '"+Temperature2+"', '"+Humidity2+"','"+Temperature3+"', '"+Humidity3+"','"+Temperature4+"', '"+Humidity4+"','"+Temperature5+"', '"+Humidity5+"','"+average_temp1+"', '"+average_humid1+"') ")
        cursor.execute("INSERT INTO [Coating].[dbo].["+Coating+"](Time_get,Temperature1,Humidity1,Temperature2,Humidity2,Temperature3,Humidity3,Temperature4,Humidity4,Temperature5,Humidity5,average_temp1,average_humid1) "
                        "VALUES ('"+Time_get+"','"+Temperature1+"', '"+Humidity1+"', '"+Temperature2+"', '"+Humidity2+"','"+Temperature3+"', '"+Humidity3+"','"+Temperature4+"', '"+Humidity4+"','"+Temperature5+"', '"+Humidity5+"','"+average_temp1+"', '"+average_humid1+"') ")
        conn.commit()
    except Exception as e:
        Systemp_log(str(e), "InsertdataCoating").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify('OK'),HTTP_201_CREATED









