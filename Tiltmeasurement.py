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

TiltMeasurement = Blueprint("TiltMeasurement", __name__, url_prefix="/api/v1/TiltMeasurement")
@TiltMeasurement.post('/Save_Data_TiltMeasurement')
@swag_from('./docs/TiltMeasurement/Data_TiltMeasurement.yaml')
def Data_Save_TiltMeasurement():
    try:
        ID_Operator = request.json['ID_Operator']
        MachineNo = request.json['MachineNo']
        productname = request.json['productname']
        QR_tray = request.json['QR_tray']
        DMC = request.json['DMC']
        Time_start = request.json['Time_start']
        Time_finish = request.json['Time_finish']
        Total_deviation = request.json['Total_deviation']
        Distance = request.json['Distance']
        Angle = request.json['Angle']
        H1 = request.json['H1']
        H2 = request.json['H2']
        H3 = request.json['H3']
        H4 = request.json['H4']
        H5 = request.json['H5']
        Result = request.json['Result']
        Status = request.json['Status']
        Picture = request.json['Picture']
        Note = request.json['Note']
        cursor.execute(
                    '''INSERT INTO [QC].[dbo].[TiltMeasurement] (ID_Operator, MachineNo, Nameproduct, QR_tray, DMC, Time_start, Time_finish, Total_deviation_height_of_A_datum, Distance_from_M_datum_to_line_of_2_pins_center, Angle_of_part_vs_master, Height_1_of_A_datum, Height_2_of_A_datum, Height_3_of_A_datum, Height_4_of_A_datum, Height_5_of_A_datum, Result, Status, Picture, Note)VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ''',
                    ID_Operator,
                    MachineNo, 
                    productname,
                    QR_tray,
                    DMC,               
                    Time_start,
                    Time_finish,
                    Total_deviation,
                    Distance,
                    Angle,
                    H1,
                    H2,
                    H3,
                    H4,
                    H5,
                    Result,
                    Status,
                    Picture,
                    Note
                )
        conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Save_Data_TiltMeasurement").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"), HTTP_201_CREATED

@TiltMeasurement.get("/showdata/<string:DMC>")
@swag_from("./docs/TiltMeasurement/Showdata.yaml")
def showdata_TiltMeasurement(DMC):
     print("select * from [QC].[dbo].[TiltMeasurement] where DMC = '"+DMC+"' and Result = 'OK' ")
     cursor.execute("select * from [QC].[dbo].[TiltMeasurement] where DMC = '"+DMC+"' and Result = 'OK' ")
     Data = cursor.fetchall()
     if len(Data)!=0:
        return jsonify("False"), HTTP_200_OK
     else:
        return jsonify("True"), HTTP_200_OK