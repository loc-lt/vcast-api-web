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

Casting = Blueprint("Casting", __name__, url_prefix="/api/v1/Casting")
@Casting.post('/Insertdata')
@swag_from('./docs/Casting/Set_data_Casting.yaml')
def Insert_data():
    try:
        Position = request.json['Position']
        Time_in = request.json['Time_in']
        Time_out = request.json['Time_out']
        Zouhbo = request.json['Zouhbo']
        MTM = request.json['MTM']
        cursor.execute("INSERT INTO [Auto].[dbo].[Casting_Auto_X5](Position,Time_in,Time_out,Zouhbo,MTemp) VALUES ('"+Position+"', '"+Time_in+"', '"+Time_out+"', '"+Zouhbo+"','"+MTM+"') ")
        conn.commit()
    except Exception as e:
        Systemp_log(str(e), "InsertdataCasting").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify('OK'),HTTP_201_CREATED
@Casting.post('/InsertTemp')
@swag_from('./docs/Casting/DataTemp_Casting.yaml')
def Insert_Temp():
    try:
        Time_get = request.json['Time_get']
        Temp_settingA = request.json['Temp_settingA']
        Temp_presentA = request.json['Temp_presentA']
        Temp_settingB = request.json['Temp_settingB']
        Temp_presentB = request.json['Temp_presentB']
        Status = request.json['Status']
        cursor.execute("INSERT INTO [Auto].[dbo].[DataTemp_Auto_X5](Time_get,Temp_settingA,Temp_presentA,Temp_settingB,Temp_presentB,Status) VALUES ('"+Time_get+"','"+Temp_settingA+"', '"+Temp_presentA+"', '"+Temp_settingB+"', '"+Temp_presentB+"','"+Status+"') ")
        conn.commit()
    except Exception as e:
        Systemp_log(str(e), "InsertdataCasting").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify('OK'),HTTP_201_CREATED









