from os import access
from constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
from flask import Blueprint, app, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flasgger import swag_from
from database import *

Airtight = Blueprint("Airtight", __name__, url_prefix="/api/v1/Airtight")


@Airtight.post('/Save_Data_Airtight')
@swag_from('./docs/Airtight/Save_Data_Airtight.yaml')
def Save_Data_Airtight():
    try:
        Machine = request.json['Machine']
        Barcode = request.json['Barcode']
        Product_type = request.json['Product_type']
        Position = request.json['Position']
        Air_value= request.json['Air_value']
        Quality =  request.json['Quality']
        Time_Start = request.json['Time_Start']
        Time_Finish = request.json['Time_Finish']
        cursor.execute("""INSERT INTO air_tight(Machine,Product_type,Barcode,Position,Air_value,Quality,Time_Start,Time_Finish) VALUES (?,?,?,?,?,?,?,?) """,
                       (Machine,Product_type,Barcode,Position,Air_value,Quality,Time_Start,Time_Finish)
                       )
        conn.commit()
        Air = {'Machine': Machine, 'Barcode':Barcode, "Position ":Position, "Air_value":Air_value, "Quality":Quality,"Time_Start":Time_Start,"Time_Finish":Time_Finish}
        return jsonify('OK'),HTTP_201_CREATED
    except:
        return jsonify({"Error": "Invalid request, please try again."})

@Airtight.post('/Save_Data_Airtight_Chamfer')
@swag_from('./docs/Airtight/Save_Data_Airtight_Chamfer.yaml')
def Save_Data_Airtight_Chamfer():
    try:
        Machine = request.json['Machine']
        Barcode = request.json['Barcode']
        Product_type = request.json['Product_type']
        Position = request.json['Position']
        Air_value= request.json['Air_value']
        Quality =  request.json['Quality']
        Time_Start = request.json['Time_Start']
        Time_Finish = request.json['Time_Finish']
        Note = request.json['Note']
        cursor.execute("""INSERT INTO air_tight_chamfer(Machine,Product_type,Barcode,Position,Air_value,Quality,Time_Start,Time_Finish,Note) VALUES (?,?,?,?,?,?,?,?,?) """,
                       (Machine,Product_type,Barcode,Position,Air_value,Quality,Time_Start,Time_Finish,Note)
                       )
        conn.commit()
        Air = {'Machine': Machine, 'Barcode':Barcode, "Position ":Position, "Air_value":Air_value, "Quality":Quality,"Time_Start":Time_Start,"Time_Finish":Time_Finish}
        return jsonify('OK'),HTTP_201_CREATED
    except:
        return jsonify({"Error": "Invalid request, please try again."})

@Airtight.post('/Save_Data_Airtight_Han')
@swag_from('./docs/Airtight/Save_Data_Airtight_Han.yaml')
def Save_Data_Airtight_Han():
    try:
        Machine = request.json['Machine']
        Barcode = request.json['Barcode']
        Position = request.json['Position']
        Air_value= request.json['Air_value']
        Quality =  request.json['Quality']
        Time_Start = request.json['Time_Start']
        Time_Finish = request.json['Time_Finish']
        Note = request.json['Note']
        cursor.execute("""INSERT INTO air_tight_han(Machine,Barcode,Position,Air_value,Quality,Time_Start,Time_Finish,Note) VALUES (?,?,?,?,?,?,?,?) """,
                       (Machine,Barcode,Position,Air_value,Quality,Time_Start,Time_Finish,Note)
                       )
        conn.commit()
        Air = {'Machine': Machine, 'Barcode':Barcode, "Position ":Position, "Air_value":Air_value, "Quality":Quality,"Time_Start":Time_Start,"Time_Finish":Time_Finish}
        return jsonify('OK'),HTTP_201_CREATED
    except:
        return jsonify({"Error": "Invalid request, please try again."})

@Airtight.post('/Save_Data_Airtight_TBN')
@swag_from('./docs/Airtight/Save_Data_Airtight_TBN.yaml')
def Save_Data_Airtight_TBN():
    try:
        Machine = request.json['Machine']
        Barcode = request.json['Barcode']
        Product_type = request.json['Product_type']
        Position = request.json['Position']
        Air_value= request.json['Air_value']
        Quality =  request.json['Quality']
        Time_Start = request.json['Time_Start']
        Time_Finish = request.json['Time_Finish']
        Note = request.json['Note']
        cursor.execute("""INSERT INTO air_tight_spain(Machine,Product_type,Barcode,Position,Air_value,Quality,Time_Start,Time_Finish,Note) VALUES (?,?,?,?,?,?,?,?,?) """,
                       (Machine,Product_type,Barcode,Position,Air_value,Quality,Time_Start,Time_Finish,Note)
                       )
        conn.commit()
        Air = {'Machine': Machine, 'Barcode':Barcode, "Position ":Position, "Air_value":Air_value, "Quality":Quality,"Time_Start":Time_Start,"Time_Finish":Time_Finish}
        return jsonify('OK'),HTTP_201_CREATED
    except:
        return jsonify({"Error": "Invalid request, please try again."})

@Airtight.get("/show")
@swag_from("./docs/Airtight/Data_Airtight.yaml")
def show():
     cursor.execute("Select*From air_tight")
     Data = cursor.fetchall()
     result=Dataget_Airtight.dump(Data)
     return jsonify({'data':result}), HTTP_200_OK
@Airtight.get("/Check_data_airtight/<string:DMC>")
@swag_from("./docs/Airtight/Check_data.yaml")
def Check_data(DMC):
     # thuc=pd.read_sql("Select*From Serial_laser",conn)
     try:
         cursor.execute("select count(id) FROM [QC].[dbo].[air_tight] where Barcode ='"+DMC+"' and Quality='OK'")
         Data = cursor.fetchone()
         if Data[0]!=0:
             return jsonify("True"), HTTP_200_OK
         else:
             cursor.execute(
                 "select count(id) FROM [QC_SWVN].[dbo].[airtight_StrongWay] where Barcode ='" + DMC + "' and Quality='OK'")
             Data = cursor.fetchone()
             if Data[0] != 0:
                 return jsonify("True"), HTTP_200_OK
             else:
                 return jsonify("False"), HTTP_200_OK
     except Exception as e:
         return jsonify({"Error": "Invalid request, please try again."})
@Airtight.post('/Save_Data_Air_Tight_Window')
@swag_from('./docs/Airtight/Save_Data_Air_Tight_Window.yaml')
def Save_Data_Air_Tight_Window():
    try:
        Product_Name = request.json['Product_Name'] 
        Barcode = request.json['Barcode']
        Airvalue_1 = request.json['Airvalue_1']
        Status_Position_1 = request.json['Status_Position_1']
        Time_Start_1 = request.json['Time_Start_1']
        Time_Finish_1 = request.json['Time_Finish_1']
        Airvalue_2 = request.json['Airvalue_2']
        Status_Position_2 = request.json['Status_Position_2']
        Time_Start_2 = request.json['Time_Start_2']
        Time_Finish_2 = request.json['Time_Finish_2']
        Note = request.json['Note']

        print("INSERT INTO [QC].[dbo].[air_tight_window](Product_Name, Barcode, Airvalue_1, Status_Position_1, Time_Start_1, Time_Finish_1, Airvalue_2, Status_Position_2, Time_Start_2, Time_Finish_2, Note) VALUES ('" + Product_Name + "', '" + Barcode + "', '" + Airvalue_1 + "', '" + Status_Position_1 +"', '" + Time_Start_1 +"', '" + Time_Finish_1 +"', '" + Airvalue_2 +"', '" + Status_Position_2 +"', '" + Time_Start_2 +"', '" + Time_Finish_2 +"', '" + Note +"')")
        cursor.execute("INSERT INTO [QC].[dbo].[air_tight_window](Product_Name, Barcode, Airvalue_1, Status_Position_1, Time_Start_1, Time_Finish_1, Airvalue_2, Status_Position_2, Time_Start_2, Time_Finish_2, Note) VALUES ('" + Product_Name + "', '" + Barcode + "', '" + Airvalue_1 + "', '" + Status_Position_1 +"', '" + Time_Start_1 +"', '" + Time_Finish_1 +"', '" + Airvalue_2 +"', '" + Status_Position_2 +"', '" + Time_Start_2 +"', '" + Time_Finish_2 +"', '" + Note +"')")
        conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Save_Data_Air_Tight_Window").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify('OK'), HTTP_201_CREATED
