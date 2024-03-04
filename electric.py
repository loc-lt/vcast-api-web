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
import datetime
dt=datetime.datetime.now()

Elec = Blueprint("Elec", __name__, url_prefix="/api/v1/Electric")
@Elec.post('/Elec_Insert')
@swag_from('./docs/Electrical/Insert_data_elec.yaml')
def Insert_data():
    try:
        Area = request.json['Area']
        Time_get=request.json['Time_get']
        Voltage = request.json['Voltage']
        Current = request.json['Current']
        Power = request.json['Power']
        PowerF = request.json['PowerF']
        Total = request.json['Total']
        Cost = request.json['Cost']
        Uab = request.json['Uab']
        Ubc = request.json['Ubc']
        Uca = request.json['Uca']
        Ia = request.json['Ia']
        Ib = request.json['Ib']
        Ic = request.json['Ic']
        current_time = dt.strftime("%H:%M:%S")
        if dt.weekday() != 7:
            # giờ binh thường
            if (current_time > '04:05:00' and current_time < '09:35:00') or (
                    current_time > '11:35:00' and current_time < '17:05:00') or (
                    current_time > '20:05:00' and current_time < '22:05:00'):
                etype = 2
            # giờ cao điểm
            elif (current_time > '09:35:00' and current_time < '11:35:00') or (
                    current_time > '17:05:00' and current_time < '20:05:00'):
                etype = 3
            # giờ thấp điểm
            else:
                etype = 1
        # chủ nhật
        else:
            # giờ binh thường
            if (current_time > '04:05:00' and current_time < '22:05:00'):
                etype = 2
            # giờ thấp điểm
            else:
                etype = 1
        cursor.execute(
            "select top(1) Total,Cost FROM [Electric].[dbo].[ELec_main] where Name_Area = '" + Area + "' order by ID desc")
        Data = cursor.fetchall()
        cursor.execute('''INSERT INTO [Electric].[dbo].[ELec_main] (Name_Area,Time_get,Voltage,I_avg,Power,PowerF,Total,Cost,Uab,Ubc,Uca,Ia,Ib,Ic,Ea_Sub,Cost_Sub,etype) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                                                                ''',
                       Area,
                       Time_get,
                       Voltage,
                       Current,
                       Power,
                       PowerF,
                       Total,
                       Cost,
                       Uab,
                       Ubc,
                       Uca,
                       Ia,
                       Ib,
                       Ic,
                       float(Total)-float(Data[0][0]),
                       float(Cost) - float(Data[0][1]),
                       etype
                       )
        conn.commit()
    except Exception as e:
        Systemp_log(str(e), "error read data Electric").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"),HTTP_201_CREATED

@Elec.post('/Elec_realtime')
@swag_from('./docs/Electrical/Update_data_elec.yaml')
def Update_data():
    try:
        Area = request.json['Area']
        Voltage = request.json['Voltage']
        Uab = request.json['Uab']
        Ubc = request.json['Ubc']
        Uca = request.json['Uca']
        Total = request.json['Total']

        cursor.execute("UPDATE [QC].[dbo].[Electrical] SET Voltage_avg = '" + Voltage + "',Uab = '" + Uab + "',Ubc = '" + Ubc + "',Uca = '" + Uca + "',Total = '" + Total + "',Status=1 where Area='"+Area+"'")
        conn.commit()
    except Exception as e:
        Systemp_log(str(e), "error read data Electric").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"),HTTP_201_CREATED






