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

ThreadVerification = Blueprint("ThreadVerification", __name__, url_prefix="/api/v1/ThreadVerification")



@ThreadVerification.post('/SAVE_DATA')
@swag_from('./docs/thread_verification/Data_ThreadVerification.yaml')
def Data_Save_ThreadVerification():
    try:
            OP_name = request.json['OP_name']
            Machine = request.json['Machine']
            DMC_product = request.json['DMC_product']
            try:
                ProductName = request.json['productname']
            except:
                ProductName = None
            Timestart = request.json['Timestart']
            Timefinish = request.json['Timefinish']
            Quality = request.json['Quality']
            Status = request.json['Status']
            acvalue = request.json['acvalue']
            setvalue = request.json['setvalue']
            Thread_gauge_code = request.json['Thread_gauge_code']
            Life_time = request.json['Life_time']
            Note_life_time = request.json['Note_life_time']
            Torque_H1 = request.json['Torque_H1']
            Torque_H2 = request.json['Torque_H2']
            Torque_H3 = request.json['Torque_H3']
            Torque_H4 = request.json['Torque_H4']
            Torque_H5 = request.json['Torque_H5']
            Torque_H6 = request.json['Torque_H6']
            Torque_H7 = request.json['Torque_H7']
            Torque_H8 = request.json['Torque_H8']
            Torque_H9 = request.json['Torque_H9']
            Torque_H10 = request.json['Torque_H10']
            Torque_H11 = request.json['Torque_H11']
            cursor.execute('''INSERT INTO [QC].[dbo].[ThreadVerification] (OP_name, Machine,ProductName, DMC_product,  Timestart, Timefinish, Quality, Status,Actual_Measured_Value,Setting_Value, Thread_gauge_code, [Life_time], Note_life_time, [Torque_H1], [Torque_H2], [Torque_H3], [Torque_H4], [Torque_H5], [Torque_H6], [Torque_H7], [Torque_H8], [Torque_H9], [Torque_H10], [Torque_H11])VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ''',
                    OP_name,
                    Machine,
                    ProductName ,
                    DMC_product,
                    Timestart ,
                    Timefinish ,
                    Quality,
                    Status,
                    acvalue,
                    setvalue,      
                    Thread_gauge_code ,
                    Life_time ,
                    Note_life_time ,
                    Torque_H1 ,
                    Torque_H2 ,
                    Torque_H3,
                    Torque_H4 ,
                    Torque_H5 ,
                    Torque_H6,
                    Torque_H7,
                    Torque_H8 ,
                    Torque_H9 ,
                    Torque_H10 ,
                    Torque_H11
            )
            conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Save_Data_ThreadVerification").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"), HTTP_201_CREATED

@ThreadVerification.post('/Update_Data_TV_DB_V1')
@swag_from('./docs/thread_verification/Update_DataTV_DB_V1.yaml')
def Update_DataTV_DB_V1():
    try:
            column = request.json['column']
            value = request.json['pallet_num']
            machineno = request.json['machineno']
            cursor.execute("update [QC].[dbo].[TV_DB] Set "+column+"="+value+" where MachineNo = '"+machineno+"'")
            conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Update_Data_TV_DB_V1").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"), HTTP_201_CREATED

@ThreadVerification.post('/Update_Data_TV_DB_V2')
@swag_from('./docs/thread_verification/Update_DataTV_DB_V2.yaml')
def Update_DataTV_DB_V2():
    try:
            column = request.json['column']
            machineno = request.json['machineno']
            cursor.execute("update [QC].[dbo].[TV_DB] Set "+column+"= '"+str(datetime.datetime.now())[:-3]+"' where MachineNo = '"+machineno+"'")
            conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Update_Data_TV_DB_V2").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"), HTTP_201_CREATED

@ThreadVerification.post('/Update_Data_TV_DB_V3')
@swag_from('./docs/thread_verification/Update_DataTV_DB_V3.yaml')
def Update_DataTV_DB_V3():
    try:
            newresult = request.json['newresult']
            dmcproduct = request.json['dmcproduct']
            #timefinish = request.json['timefinish']
            cursor.execute("update [QC].[dbo].[ThreadVerification] Set Quality = '"+newresult+"', Timefinish = '"+str(datetime.datetime.now())[:-3]+"' where DMC_product = '"+dmcproduct+"'")
            
            #print("update [QC].[dbo].[ThreadVerification] Set Quality = '"+newresult+"', Timefinish = '"+str(datetime.datetime.now())[:-3]+"' where DMC_product = '"+dmcproduct+"'")
            conn.commit()
            row_count = cursor.rowcount
            print("Số lượng dòng đã được cập nhật:", row_count)
    except Exception as e:
        Systemp_log(str(e), "Update_Data_TV_DB_V3").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify(str(row_count)), HTTP_201_CREATED

@ThreadVerification.post('/Update_Data_TV_DB_V4')
@swag_from('./docs/thread_verification/Update_DataTV_DB_V4.yaml')
def Update_DataTV_DB_V4():
    try:
            number1 = request.json['number1']
            b = request.json['b']
            
            cursor.execute("UPDATE [QC].[dbo].[2D_Thread] set  Hole_no = '"+str(number1)+"',  Hole_tor"+str(number1)+" =  '"+str(b)+"' where id = 2")
            conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Update_Data_TV_DB_V4").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"), HTTP_201_CREATED

@ThreadVerification.post('/Update_Data_TV_DB_V5')
@swag_from('./docs/thread_verification/Update_DataTV_DB_V5.yaml')
def Update_DataTV_DB_V5():
    try:
            number1 = request.json['number1']
            d = request.json['d']
            
            cursor.execute("UPDATE [QC].[dbo].[2D_Thread] set  Hole_no = '"+str(number1)+"', Hole_stt"+str(number1)+" =  '"+str(d)+"' where  id = 2")
            conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Update_Data_TV_DB_V5").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"), HTTP_201_CREATED

@ThreadVerification.post('/Update_Data_TV_DB_V6')
@swag_from('./docs/thread_verification/Update_DataTV_DB_V6.yaml')
def Update_DataTV_DB_V6():
    try:
            dmc_2d = request.json['dmc_2d']
            typepr = request.json['typepr']
            
            cursor.execute("UPDATE [QC].[dbo].[2D_Thread] set DMC ='"+dmc_2d+"', Product_type = '"+typepr+"'   where id = 2")
            conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Update_Data_TV_DB_V6").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"), HTTP_201_CREATED

@ThreadVerification.post('/Update_Data_TV_DB_V7')
@swag_from('./docs/thread_verification/Update_DataTV_DB_V7.yaml')
def Update_DataTV_DB_V7():
    try:
            number1 = request.json['number1']
            b = request.json['b']
            
            cursor.execute("UPDATE [QC].[dbo].[2D_Thread] set  Hole_no = '"+str(number1)+"',  Hole_tor"+str(number1)+" =  '"+str(b)+"' where id = 1")
            conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Update_Data_TV_DB_V7").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"), HTTP_201_CREATED

@ThreadVerification.post('/Update_Data_TV_DB_V8')
@swag_from('./docs/thread_verification/Update_DataTV_DB_V8.yaml')
def Update_DataTV_DB_V8():
    try:
            number1 = request.json['number1']
            d = request.json['d']
            
            cursor.execute("UPDATE [QC].[dbo].[2D_Thread] set  Hole_no = '"+str(number1)+"', Hole_stt"+str(number1)+" =  '"+str(d)+"' where  id = 1")
            conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Update_Data_TV_DB_V8").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"), HTTP_201_CREATED

@ThreadVerification.post('/Update_Data_TV_DB_V9')
@swag_from('./docs/thread_verification/Update_DataTV_DB_V9.yaml')
def Update_DataTV_DB_V9():
    try:
            dmc_2d = request.json['dmc_2d']
            typepr = request.json['typepr']
            
            cursor.execute("UPDATE [QC].[dbo].[2D_Thread] set DMC ='"+dmc_2d+"', Product_type = '"+typepr+"'   where id = 1")
            conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Update_Data_TV_DB_V9").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"), HTTP_201_CREATED

@ThreadVerification.post('/Update_Data_TV_DB_V10')
@swag_from('./docs/thread_verification/Update_DataTV_DB_V10.yaml')
def Update_DataTV_DB_V10():
    try:
            dmc_2d = request.json['dmc_2d']
            typepr = request.json['typepr']
            machine =  request.json['machine']
            cursor.execute("UPDATE [QC].[dbo].[2D_Thread] set DMC ='"+dmc_2d+"', Product_type = '"+typepr+"'   where Machineno = '"+machine+"'")
            conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Update_Data_TV_DB_V10").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"), HTTP_201_CREATED

@ThreadVerification.post('/Update_Data_TV_DB_V11')
@swag_from('./docs/thread_verification/Update_DataTV_DB_V11.yaml')
def Update_DataTV_DB_V11():
    try:
            number1 = request.json['number1']
            d = request.json['d']
            machine =  request.json['machine']
            cursor.execute("UPDATE [QC].[dbo].[2D_Thread] set  Hole_no = '"+str(number1)+"', Hole_stt"+str(number1)+" =  '"+str(d)+"' where Machineno = '"+machine+"'")
            conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Update_Data_TV_DB_V11").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"), HTTP_201_CREATED

@ThreadVerification.post('/Update_Data_TV_DB_V12')
@swag_from('./docs/thread_verification/Update_DataTV_DB_V12.yaml')
def Update_DataTV_DB_V12():
    try:
            number1 = request.json['number1']
            b = request.json['b']
            machine =  request.json['machine']
            cursor.execute("UPDATE [QC].[dbo].[2D_Thread] set  Hole_no = '"+str(number1)+"',  Hole_tor"+str(number1)+" =  '"+str(b)+"' where Machineno = '"+machine+"'")
            conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Update_Data_TV_DB_V12").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"), HTTP_201_CREATED

@ThreadVerification.get("/Setting")
@swag_from("./docs/thread_verification/Setting.yaml")
def showsetting():
     cursor.execute("SELECT * FROM [QC].[dbo].[TV_DB]")
     Data = cursor.fetchall()
     result=Settings_TVDB.dump(Data)
     return jsonify({'data':result}), HTTP_200_OK




@ThreadVerification.get("/showdata/<string:DMC_product>")
@swag_from("./docs/thread_verification/Showdata.yaml")
def showdata_thread_verification(DMC_product):
     print("select * from ThreadVerification where DMC_product = '"+DMC_product+"' and Quality = 'OK' ")
     cursor.execute("select * from ThreadVerification where DMC_product = '"+DMC_product+"' and Quality = 'OK' ")
     Data = cursor.fetchall()
     if len(Data)!=0:
        return jsonify("False"), HTTP_200_OK
     else:
        return jsonify("True"), HTTP_200_OK





