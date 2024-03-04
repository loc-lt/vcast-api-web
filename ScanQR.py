from os import access
from constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
from flask import Blueprint, app, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flasgger import swag_from
from database import *
from ERROR import *
ScanQR = Blueprint("ScanQR", __name__, url_prefix="/api/v1/ScanQR")

def CheckDMCFixture(valueDMC, SET):
    if str(valueDMC).isdigit():
        if SET=="SET7" or SET=="SET8":
            cursor.execute(
                "select *From [QC].[dbo].[SETTING_CNC] where "+SET+" = "+valueDMC[-3:]+" or OK1 = "+valueDMC[-3:]+" ")
            Data = cursor.fetchall()
            if len(Data)!=0:
                return True
        else:
            cursor.execute(
                "select *From [QC].[dbo].[SETTING_CNC] where " + SET + " = " + valueDMC[-3:] + " or OK = " + valueDMC[-3:] + " ")
            Data = cursor.fetchall()
            if len(Data) != 0:
                return True
    return False
@ScanQR.post('/Save_Data_ScanQR')
@swag_from('./docs/ScanQR/Save_Data_ScanQR.yaml')
def Save_Data_ScanQR():
    try:
        Product = request.json['Product']
        Time_scan_product = request.json['Time_scan_product']
        Time_scan_tray = request.json['Time_scan_tray']
        DMC_product= request.json['DMC_product']
        DMC_tray =  request.json['DMC_tray']
        Compare = request.json['Compare']
        cursor.execute("""INSERT INTO ScanQR(Product,Time_scan_product,Time_scan_tray,DMC_product,DMC_tray,Compare) VALUES (?,?,?,?,?,?) """,
                       (Product,Time_scan_product,Time_scan_tray,DMC_product,DMC_tray,Compare)
                       )
        conn.commit()
    except Exception as e:
        Systemp_log(str(e), "set_serial").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify('OK'), HTTP_201_CREATED

@ScanQR.get("/show")
@swag_from("./docs/ScanQR/Data_ScanQR.yaml")
def show():
    try:
     cursor.execute("SELECT TOP (33)* FROM ScanQR order by Time_scan_product desc")
     Data = cursor.fetchall()
     result=Dataget_QR.dump(Data)
     print(Data)
    except Exception as e:
        Systemp_log(str(e), "GetDataScanQR").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify({'data': result}), HTTP_200_OK

@ScanQR.get("/get_Data_ScanQR/<string:DMC_Product>")
@swag_from("./docs/ScanQR/Get_Data_ScanQR.yaml")
def get_Data_ScanQR(DMC_Product):
    try:
         # thuc=pd.read_sql("Select*From Serial_laser",conn)
         cursor.execute("SELECT * FROM ScanQR where DMC_product LIKE '%"+DMC_Product+"%'ORDER BY Time_scan_product DESC")
         Data = cursor.fetchall()
         result=Dataget_QR.dump(Data)
    except Exception as e:
        Systemp_log(str(e), "get_Data_ScanQR").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify({'data':result}), HTTP_200_OK
@ScanQR.post("/Get_DMC_product")
@swag_from("./docs/ScanQR/Get_DMC_product.yaml")
def Get_DMC_product():
    try:
         Product = request.json['Product']
         DMC_tray = request.json['DMC_tray']
         SET = request.json['SET']
         #cursor.execute("select top(1) Product,DMC_product FROM [QC].[dbo].[ScanQR] where DMC_tray = '"+DMC_tray+"' and Product = '"+Product+"' and Compare='OK' order by ID desc")
         cursor.execute("select top(1) Product,DMC_product FROM [QC].[dbo].[ScanQR] where DMC_tray = '"+DMC_tray+"' and DMC_product  like'%A%' and Compare='OK' order by ID desc")
         #cursor.execute("select product,dmc_product from (SELECT TOP (1) *,RANK () OVER (PARTITION BY [DMC_tray]  ORDER BY id desc ) rank_no FROM [QC].[dbo].[ScanQR]  where DMC_tray= '"+DMC_tray+"'   and compare = 'ok' ) as a where rank_no = 1 and [DMC_product] like '%A' ")

         Data = cursor.fetchall()
         
         if len(Data)==0 :
             return jsonify("False")#error barcode
         else:
             cursor.execute("select count(ID) FROM [QC].[dbo].[CNC] where DMC_product like'" + Data[0][1].strip() + "'")
             Data1 = cursor.fetchone()
             if Data1[0] == 0:
                 result=Products_QR.dump(Data)
                 return jsonify({'data':result})
             else:
                 return jsonify("False")

    except Exception as e:
        Systemp_log(str(e), "Check_castingname").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})

@ScanQR.post("/Check_DMC_product")
@swag_from("./docs/ScanQR/Check_DMC_product.yaml")
def Check_DMC_product():
    try:
         Product = request.json['Product']
         DMC_tray = request.json['DMC_tray']
         SET = request.json['SET']
         #cursor.execute("select top(1) Product,DMC_product FROM [QC].[dbo].[ScanQR] where DMC_tray = '"+DMC_tray+"' and Product = '"+Product+"' and Compare='OK' order by ID desc")
         cursor.execute("select top(1) Product,DMC_product FROM [QC].[dbo].[ScanQR] where DMC_tray = '"+DMC_tray+"' and DMC_product  like'%A%' and Compare='OK' order by ID desc")
         #cursor.execute("select product,dmc_product from (SELECT TOP (1) *,RANK () OVER (PARTITION BY [DMC_tray]  ORDER BY id desc ) rank_no FROM [QC].[dbo].[ScanQR]  where DMC_tray= '"+DMC_tray+"'   and compare = 'ok' ) as a where rank_no = 1 and [DMC_product] like '%A' ")
         Data = cursor.fetchall()
         if len(Data)==0 :
             return jsonify("False1")#error barcode
         else:
             cursor.execute("select count(ID) FROM [QC].[dbo].[CNC] where DMC_product like'" + Data[0][1].strip() + "'")
             Data1 = cursor.fetchone()
             if Data1[0] != 0 and CheckDMCFixture(DMC_tray, SET) == False:
                 return jsonify("False2")# Qc has not scanned and production line error
             elif Data1[0] != 0:
                return jsonify("False3"), HTTP_200_OK# Qc has not scanned
             elif Data1[0] == 0 and CheckDMCFixture(DMC_tray, SET) == False:
                 return jsonify("False4"), HTTP_200_OK# production line error
             else:
                return jsonify("True")
    except Exception as e:
        Systemp_log(str(e), "Check_castingname").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
