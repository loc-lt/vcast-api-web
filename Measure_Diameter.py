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

Measure_Diameter = Blueprint("Measure_Diameter", __name__, url_prefix="/api/v1/Measure_Diameter")

@Measure_Diameter.post('/Insert_Measure_Diameter')
@swag_from('./docs/Measure_Diameter/Data_Measure_Diameter.yaml')
def Insert_Measure_Diameter():
    try:
        Product_Name = request.json['Product_Name']
        Time_ScanDMC = request.json['Time_ScanDMC']
        DMC = request.json['DMC']
        A_Min = request.json['A_Min']
        A_Max = request.json['A_Max']
        B_Min = request.json['B_Min']
        B_Max = request.json['B_Max']
        Time_Finish = request.json['Time_Finish']
        Result = request.json['Result']

        cursor.execute( "INSERT INTO [QC].[dbo].[Measure_Diameter](Product_Name,Time_ScanDMC,DMC,A_Min,A_Max,B_Min,B_Max,Time_Finish,Result) "
            "VALUES ('" + Product_Name + "','" + Time_ScanDMC + "','" + DMC + "', '" + A_Min + "', '" + A_Max + "', '" + B_Min + "','" + B_Max + "', '" + Time_Finish + "', '" + Result + "') ")
        conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Insert_Measure_Diameter").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify('OK'),HTTP_201_CREATED
@Measure_Diameter.post('/count_history_Measure_Diameter')
@swag_from('./docs/Measure_Diameter/count_history.yaml')
def count_history_Measure_Diameter():
    try:
        strtoday = request.json['strtoday']
        strnextday = request.json['strnextday']
        Result = request.json['Result']
        cursor.execute("select count(*) from [QC].[dbo].[Measure_Diameter] where Result = '"+Result+"' and Time_Finish >'" + strtoday + "'and Time_Finish < '" + strnextday+"'")
        Data=cursor.fetchall()
        count=Data[0][0]
    except Exception as e:
        Systemp_log(str(e), "count_history").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify(count),HTTP_201_CREATED

@Measure_Diameter.post('/Insert_Measure_Diameter_GC')
@swag_from('./docs/Measure_Diameter/Data_Measure_Diameter_GC.yaml')
def Insert_Measure_Diameter_GC():
    try:
        Product_Name=request.json['Product_Name']
        Time_ScanDMC = request.json['Time_ScanDMC']
        DMC = request.json['DMC']
        A_Min = request.json['A_Min']
        A_Max = request.json['A_Max']
        B_Min = request.json['B_Min']
        B_Max = request.json['B_Max']
        Time_Finish = request.json['Time_Finish']
        Result = request.json['Result']

        cursor.execute("INSERT INTO [GC].[dbo].[Measure_Diameter](Product_Name,Time_ScanDMC,DMC,A_Min,A_Max,B_Min,B_Max,Time_Finish,Result) "
                        "VALUES ('"+Product_Name+"','"+Time_ScanDMC+"','"+DMC+"', '"+A_Min+"', '"+A_Max+"', '"+B_Min+"','"+B_Max+"', '"+Time_Finish+"', '"+Result+"') ")
        conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Insert_Measure_Diameter").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify('OK'),HTTP_201_CREATED
@Measure_Diameter.post('/count_history_Measure_Diameter_GC')
@swag_from('./docs/Measure_Diameter/count_history_GC.yaml')
def count_history_Measure_Diameter_GC():
    try:
        strtoday = request.json['strtoday']
        strnextday = request.json['strnextday']
        Result = request.json['Result']
        cursor.execute("select count(*) from [GC].[dbo].[Measure_Diameter] where Result = '"+Result+"' and Time_Finish >'" + strtoday + "'and Time_Finish < '" + strnextday+"'")
        Data=cursor.fetchall()
        count=Data[0][0]
    except Exception as e:
        Systemp_log(str(e), "count_history").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify(count),HTTP_201_CREATED






