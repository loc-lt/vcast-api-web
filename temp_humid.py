from os import access
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
from flask import Blueprint, app, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flasgger import swag_from
from database import *
from ERROR import *
TH = Blueprint("TH", __name__, url_prefix="/api/v1/TempHumid")
@TH.post('/TempHumid_Insert')
@swag_from('./docs/TempHumid/Insert_data_TH.yaml')
def Insert_data():
    try:
        Area = request.json['Area']
        Time_get=request.json['Time_get']
        Temp = request.json['Temp']
        Humid = request.json['Humid']

        cursor.execute('''INSERT INTO [QC].[dbo].[Temp_Humid_Factory] (Area,Time_get,Temp,Humid) VALUES (?,?,?,?)''',
                       Area,
                       Time_get,
                       Temp,
                       Humid
                       )
        conn.commit()
    except Exception as e:
        Systemp_log(str(e), "error save data TempHumid").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"),HTTP_201_CREATED

@TH.post('/TH_realtime')
@swag_from('./docs/TempHumid/Update_data_TH.yaml')
def Update_data():
    try:
        Area = request.json['Area']
        Temp = request.json['Temp']
        Humid = request.json['Humid']
        cursor.execute("UPDATE [QC].[dbo].[Temp_Humid_realtime] SET Temp = '" + Temp + "',Humid = '" + Humid + "' where Area='"+Area+"'")
        conn.commit()
    except Exception as e:
        Systemp_log(str(e), "error Update data TempHumid ").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"),HTTP_201_CREATED

@TH.post('/TH_setting')
@swag_from('./docs/TempHumid/Update_setting_TH.yaml')
def Update_setting():
    try:
        Area = request.json['Area']
        Tempmin = request.json['Tempmin']
        Humidmin = request.json['Humidmin']
        Tempmax = request.json['Tempmax']
        Humidmax = request.json['Humidmax']
        print("UPDATE [QC].[dbo].[Temp_Humid_Setting] SET temp_min = '" + Tempmin + "',temp_max = '" + Tempmax + "',humid_min = '" + Humidmin + "',humid_max = '" + Humidmax + "' where Area='"+Area+"'")
        cursor.execute("UPDATE [QC].[dbo].[Temp_Humid_Setting] SET temp_min = '" + Tempmin + "',temp_max = '" + Tempmax + "',humid_min = '" + Humidmin + "',humid_max = '" + Humidmax + "' where Area='"+Area+"'")
        conn.commit()
    except Exception as e:
        Systemp_log(str(e), "error Update setting Temphumid ").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"),HTTP_201_CREATED




