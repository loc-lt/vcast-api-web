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

DONGBIN = Blueprint("DONGBIN", __name__, url_prefix="/api/v1/DONGBIN")


@DONGBIN.post('/Insertdata')
@swag_from('./docs/DONGBIN/Save_data_DONGBIN.yaml')
def Insert_data():
    try:
        Machineno = request.json['Machineno']
        DMC_product = request.json['DMC_product']
        MotorCurrent = request.json['MotorCurrent']
        Position = request.json['Position']
        TimeStart = request.json['TimeStart']
        TimeFinish = request.json['TimeFinish']
        Result = request.json['Result']

        # print("""INSERT INTO CNC(Machineno,DMC_product,MotorCurrent,Position,TimeStart,TimeFinish,Result) VALUES (?,?,?,?,?,?,?,?) """,
        #     (Machineno, DMC_product, MotorCurrent, Position, TimeStart,TimeFinish, Result))
        cursor.execute("""INSERT INTO DONG_BIN(Machineno,DMC_product,MotorCurrent,Position,TimeStart,TimeFinish,Result) VALUES (?,?,?,?,?,?,?) """,
            (Machineno, DMC_product, MotorCurrent, Position, TimeStart,TimeFinish, Result))
        conn.commit()
    except Exception as e:
        Systemp_log(str(e), "InsertdataDONGBIN").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify('OK'),HTTP_201_CREATED







