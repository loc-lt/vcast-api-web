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

CNC = Blueprint("CNC", __name__, url_prefix="/api/v1/CNC")


@CNC.post('/Insertdata')
@swag_from('./docs/CNC/Set_data_CNC.yaml')
def Insert_data():
    try:
        Machineno = request.json['Machineno']
        Pos_product = request.json['Pos_product']
        Name_product = request.json['Name_product']
        DMC_Fixture = request.json['DMC_Fixture']
        DMC_product = request.json['DMC_product']
        Position1 = request.json['Position1']
        TimeinCNC1 = request.json['TimeinCNC1']
        TimeoutCNC1 = request.json['TimeoutCNC1']
        StatusDMC = request.json['StatusDMC']
       
        cursor.execute("""INSERT INTO CNC(Machineno,Pos_product,Name_product,DMC_Fixture,DMC_product,Position1,TimeinCNC1,TimeoutCNC1,Status) VALUES (?,?,?,?,?,?,?,?,?) """,
            (Machineno, Pos_product, Name_product, DMC_Fixture, DMC_product, Position1,TimeinCNC1, TimeoutCNC1,StatusDMC))
        conn.commit()
    except Exception as e:
        Systemp_log(str(e), "InsertdataCNC").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify('OK'),HTTP_201_CREATED

@CNC.post('/Updatedata')
@swag_from("./docs/CNC/Update_data_CNC.yaml")
def Update_Data():
     try:
         Machineno = request.json['Machineno']
         Pos_product = request.json['Pos_product']
         Position2 = request.json['Position2']
         TimeinCNC1 = request.json['TimeinCNC1']
         TimeinCNC2 = request.json['TimeinCNC2']
         TimeoutCNC2 = request.json['TimeoutCNC2']
     # thuc=pd.read_sql("Select*From Serial_laser",conn)
         cursor.execute("UPDATE CNC set Position2 = '" + Position2+ "',TimeinCNC2='" + TimeinCNC2 + "',TimeoutCNC2='" + TimeoutCNC2 + "' where Machineno = '" + Machineno + "' and Pos_product='" + Pos_product + "'and TimeinCNC1 ='" + TimeinCNC1+ "' and Position2 is NULL ")
         conn.commit()
     except Exception as e:
        Systemp_log(str(e), "Update_DataCNC").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
     return jsonify('OK'),HTTP_201_CREATED






