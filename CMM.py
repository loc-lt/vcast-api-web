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
import traceback
import pandas as pd

CMM = Blueprint("CMM", __name__, url_prefix="/api/v1/CMM")

@CMM.post('/Save_CMM')
@swag_from('./docs/CMM/SavedataCMM.yaml')
def Save_Data_CMM():
    try:
            CMMCode = request.json['CMMCode']
            TimeStart = request.json['TimeStart']
            DMC = request.json['DMC']
            TimeSave = request.json['TimeSave']
            Product = request.json['Product']
            Line = request.json['Line']
            CMMmachine = request.json['CMMmachine']
            Operator = request.json['Operator']
            CodePurpose = request.json['CodePurpose']
            MassProduction = request.json['MassProduction']
            id = request.json['id']
            actual = request.json['actual']
            nominal = request.json['nominal']
            uppertol = request.json['uppertol']
            lowertol = request.json['lowertol']
            deviation = request.json['deviation']
            exceed = request.json['exceed']
            natuppertolid = request.json['natuppertolid']
            natlowertolid = request.json['natlowertolid']
            unit = request.json['unit']
            Result = request.json['Result']
            Requester= request.json['Requester']
            cursor.execute(
                '''INSERT INTO [Qc].[dbo].[CMMdata] VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ''',
                DMC,
                TimeStart,
                TimeSave,
                Product,
                Line,
                CMMCode,
                CMMmachine,
                Operator,
                CodePurpose,
                MassProduction,
                "",
                "",
                id,
                actual,
                nominal,
                uppertol,
                lowertol,
                deviation,
                exceed,
                natuppertolid,
                natlowertolid,
                unit,
                Result,
                Requester
            )
            conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Save_Data_Classification").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"), HTTP_201_CREATED

@CMM.post('/Update_duplicate_CMM')
@swag_from('./docs/CMM/Update_duplicate.yaml')
def Update_duplicate_CMM():
    try:
            TimeSave = request.json['TimeSave']
            actual = request.json['actual']
            deviation = request.json['deviation']
            result = request.json['result']
            DMC = request.json['DMC']
            id = request.json['id']
            cursor.execute(" Update CMMdata set TimeSave = '"+TimeSave+"', actual ='"+actual+"', deviation ='"+deviation+"',result = '"+result+"' where DMC ='"+DMC+"' and id = '"+id+"'")
            conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Update_duplicate_CMM").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"), HTTP_201_CREATED

@CMM.post('/Check_Data_CMM')
@swag_from('./docs/CMM/Check_Data_CMM.yaml')
def Check_Data_CMM():
    try:
            product = request.json['product']
            DMC = request.json['DMC']
            idx = request.json['id']
            cursor.execute("select DMC from CMMdata where Product = '"+product+"' and DMC = '"+DMC+"' and id = '"+idx+"'")
            Data = cursor.fetchall()
            if len(Data)!=0:
                return jsonify("True")
            else:
                return jsonify("False")
    except Exception as e:
        Systemp_log(str(e), "Update_Data_Classification").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})

@CMM.get("/Get_Count_CMM")
@swag_from("./docs/CMM/Get_Count_CMM.yaml")
def Get_Count_CMM():
    try:

         today = datetime.datetime.now()
         ytday = today - datetime.timedelta(days=1)
         if today.hour < 8:
             cursor.execute("select count(distinct(DMC)) as count from [QC].[dbo].[CMMdata] where TimeSave > '" + ytday.strftime(
                     "%Y-%m-%d 20:00:00'"))
             ok_count = cursor.fetchone()[0]
         else:
             cursor.execute(
                 "select count(distinct(DMC)) as count from [QC].[dbo].[CMMdata] where TimeSave > '" + today.strftime(
                     "%Y-%m-%d 08:00:00'"))
             ok_count = cursor.fetchone()[0]
    except Exception as e:
        Systemp_log(str(e), "get_Data_ScanQR").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify(ok_count), HTTP_200_OK

@CMM.post('/Check_Count_CMM')
@swag_from('./docs/CMM/Check_Count_CMM.yaml')
def Check_Count_CMM():
    try:
            CMMmachine = request.json['CMMmachine']
            DMC = request.json['DMC']
            Operator = request.json['Operator']
            cursor.execute("select count(IDx) from cmmdata where DMC='"+DMC+"' and CMMmachine='"+CMMmachine+"' and Operator ='"+Operator+"'")
            count = cursor.fetchone()[0]
    except Exception as e:
        Systemp_log(str(e), "Update_Data_Classification").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return  jsonify(count)

@CMM.post('/Read_Data')
@swag_from('./docs/CMM/Read_Data.yaml')
def Read_Data():
    try:
            DMC = request.json['DMC']
            id = request.json['id']
            print("select actual, Result from [QC].[dbo].[CMMdata] where DMC like '%" + DMC +"%' and id = '" + id+ "'")
            cursor.execute("select actual, Result from [QC].[dbo].[CMMdata] where DMC like '%" + DMC +"%' and id = '" + id+ "'")
            Data = cursor.fetchall()
            print(Data)
            # result=Dataget_Waxmold.dump(Data)
    except Exception as e:
        Systemp_log(str(e), "Read_Data").append_new_line()
    return jsonify({'value':str(round(float(Data[0][0]),3)),"result":Data[0][1].strip()}), HTTP_200_OK

@CMM.post('/Save_CMM_New')
@swag_from('./docs/CMM/SaveCMMDataNew.yaml')
def Save_Data_CMM_New():
    try:
        DMC = request.json['DMC']
        TimeStart = request.json['TimeStart']
        TimeSave = request.json['TimeSave']
        Product = request.json['Product']
        Line = request.json['Line']
        CMMCode = request.json['CMMCode']
        CMMMachine = request.json['CMMMachine']
        Operator = request.json['Operator']
        CodePurpose = request.json['CodePurpose']
        MassProduction = request.json['MassProduction']
        ID = request.json['ID']
        Actual = request.json['Actual']
        Nominal = request.json['Nominal']
        Uppertol = request.json['Uppertol']
        Lowertol = request.json['Lowertol']
        Deviation = request.json['Deviation']
        Exceed = request.json['Exceed']
        Result = request.json['Result']
        Requester= request.json['Requester']

        print("INSERT INTO [Qc].[dbo].[CMMdata](DMC, TimeStart, TimeSave, Product, Line, CMMCode, CMMMachine, Operator, CodePurpose, MassProduction, ID, Actual, Nominal, Uppertol, Lowertol, Deviation, Exceed, Result, Requester) VALUES ('"+ DMC +"','"+ TimeStart +"','"+ TimeSave +"','"+ Product +"','"+ Line +"','"+ CMMCode +"','"+ CMMMachine +"','"+ Operator +"','"+ CodePurpose +"','"+ MassProduction +"','"+ ID +"','"+ Actual +"','"+ Nominal +"','"+ Uppertol +"','"+ Lowertol +"','"+ Deviation +"','"+ Exceed +"','"+ Result +"','"+ Requester +"')")
        cursor.execute("INSERT INTO [Qc].[dbo].[CMMdata](DMC, TimeStart, TimeSave, Product, Line, CMMCode, CMMMachine, Operator, CodePurpose, MassProduction, ID, Actual, Nominal, Uppertol, Lowertol, Deviation, Exceed, Result, Requester) VALUES ('"+ DMC +"','"+ TimeStart +"','"+ TimeSave +"','"+ Product +"','"+ Line +"','"+ CMMCode +"','"+ CMMMachine +"','"+ Operator +"','"+ CodePurpose +"','"+ MassProduction +"','"+ ID +"','"+ Actual +"','"+ Nominal +"','"+ Uppertol +"','"+ Lowertol +"','"+ Deviation +"','"+ Exceed +"','"+ Result +"','"+ Requester +"')")
        
        conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Save_Data_CMM_New").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"), HTTP_201_CREATED

# Viết lại các api cho A. Hiển
# Lấy danh sách tất cả product
@CMM.get('/products') 
@swag_from('./docs/CMM/get_products.yaml')
def get_products():
    try:
        # Tạo cusor để kết nối với database
        conn = pyodbc.connect('Driver={SQL Server}; Server=192.168.8.21; uid=sa; pwd=1234;Database=QC; Trusted_Connection=No;',timeout=1)
        cursor = conn.cursor()

        cursor.execute("select distinct(Product) as Product from CMMData order by Product")
        product_list = cursor.fetchall()

        # Nếu lấy dữ liệu ra trống
        if product_list == None:
            ret = {
                'status':False,
                'message':'Not Exist Data'
            }
            return jsonify(ret),400

        # Nếu all_records được truy vấn thành công
        ret = {
                'status':True,
                'message':'Success',
                'data': []
            }
        
        if len(product_list) == 0:
            ret['data'] = None                  
            return jsonify(ret)
    

        for item in product_list:
            file_name = item
            ret["data"].append(file_name[0])
        
        return jsonify(ret)
    except Exception as e:
        ret = {
            'status':False,
            'message': str(e)
        }
        Systemp_log(traceback.format_exc(), "products").append_new_line()
        return jsonify(ret),500
    
@CMM.get('/machines') 
@swag_from('./docs/CMM/get_machines.yaml')
def get_machines():
    try:
        # Tạo cusor để kết nối với database
        conn = pyodbc.connect('Driver={SQL Server}; Server=192.168.8.21; uid=sa; pwd=1234;Database=QC; Trusted_Connection=No;',timeout=1)
        cursor = conn.cursor()

        cursor.execute("select distinct(CMMmachine) as Product from CMMData order by CMMmachine")
        machine_list = cursor.fetchall()

        # Nếu lấy dữ liệu ra trống
        if machine_list == None:
            ret = {
                'status':False,
                'message':'Not Exist Data'
            }
            return jsonify(ret),400

        # Nếu all_records được truy vấn thành công
        ret = {
                'status':True,
                'message':'Success',
                'data': []
            }
        
        if len(machine_list) == 0:
            ret['data'] = None                  
            return jsonify(ret)
    

        for item in machine_list:
            file_name = item
            ret["data"].append(file_name[0])
        
        return jsonify(ret)
    except Exception as e:
        ret = {
            'status':False,
            'message': str(e)
        }
        Systemp_log(traceback.format_exc(), "machines").append_new_line()
        return jsonify(ret),500
    
@CMM.get('/forms') 
@swag_from('./docs/CMM/get_forms.yaml')
def get_forms():
    try:
        # Tạo cusor để kết nối với database
        conn = pyodbc.connect('Driver={SQL Server}; Server=192.168.8.21; uid=sa; pwd=1234;Database=QC; Trusted_Connection=No;',timeout=1)
        cursor = conn.cursor()

        cursor.execute("select distinct(FormName) as Fname from CMMFormData")
        form_list = cursor.fetchall()

        # Nếu lấy dữ liệu ra trống
        if form_list == None:
            ret = {
                'status':False,
                'message':'Not Exist Data'
            }
            return jsonify(ret),400

        # Nếu all_records được truy vấn thành công
        ret = {
                'status':True,
                'message':'Success',
                'data': []
            }
        
        if len(form_list) == 0:
            ret['data'] = None                  
            return jsonify(ret)
    

        for item in form_list:
            file_name = item
            ret["data"].append(file_name[0])
        
        return jsonify(ret)
    except Exception as e:
        ret = {
            'status':False,
            'message': str(e)
        }
        Systemp_log(traceback.format_exc(), "forms").append_new_line()
        return jsonify(ret),500
    
@CMM.post('') 
@swag_from('./docs/CMM/data.yaml')
def get_data():
    try:
        # Tạo cusor để kết nối với database
        conn = pyodbc.connect('Driver={SQL Server}; Server=192.168.8.21; uid=sa; pwd=1234;Database=QC; Trusted_Connection=No;',timeout=1)
        cursor = conn.cursor()

        # Ngày
        day_start = request.json['dayStart']
        day_end = request.json['dayEnd']

        # Giờ
        time_start = request.json['timeStart']
        time_end = request.json['timeEnd']

        # Ngày giờ
        datetime_start = day_start + " " + time_start
        datetime_end = day_end + " " + time_end
        
        product = request.json["product"]
        machine = request.json["machine"]
        dmc = request.json["dmc"]

        print("SELECT TimeStart, TimeSave, requester, CodePurpose, DMC, Line, CMMmachine,CMMCode, Operator, (CASE WHEN (SELECT count(value) FROM STRING_SPLIT(Product, ' ')) >= 2 THEN (SELECT dbo.ConcatValuesInColumn(Product, 2)) ELSE Product END) as Product, SUM(CASE WHEN Result != '' THEN 1 ELSE 0 END) AS Total,SUM(CASE WHEN id like '%No Tol%' THEN 1 ELSE 0 END) AS NoTol, SUM(CASE WHEN id like '%In Tol%' THEN 1 ELSE 0 END) AS InTol,SUM(CASE WHEN Result = 'OK'  and id not like '%No Tol%' and id not like '%In Tol%' THEN 1 ELSE 0 END) AS OK_Total,SUM(CASE WHEN Result = 'NG' and id not like '%No Tol%' and id not like '%In Tol%' THEN 1 ELSE 0 END) AS NG_Total,SUM(CASE WHEN Result = 'OK' and id not like '%No Tol%' and id not like '%In Tol%' and (id like '% C\_%' ESCAPE '\\' or id like '% C.%' or id like '% C %' or id like '% CC %') THEN 1 ELSE 0 END) AS OK_C,SUM(CASE WHEN Result = 'NG' and id not like '%No Tol%' and id not like '%In Tol%' and (id like '% C\_%' ESCAPE '\\' or id like '% C.%'or id like '% C %' or id like '% CC %') THEN 1 ELSE 0 END) AS NG_C,SUM(CASE WHEN Result = 'OK' and id not like '%No Tol%' and id not like '%In Tol%' and id like '%CM%' THEN 1 ELSE 0 END) AS OK_CM,SUM(CASE WHEN Result = 'NG' and id not like '%No Tol%' and id not like '%In Tol%' and id like '%CM%' THEN 1 ELSE 0 END) AS NG_CM,SUM(CASE WHEN Result = 'OK' and id not like '%No Tol%' and id not like '%In Tol%' and id not like '%CM%' and id not like '% C\_%' ESCAPE '\\' and id not like '% C.%' and id not like '% C %' and id not like '% CC %' THEN 1 ELSE 0 END) AS OK_MM,SUM(CASE WHEN Result = 'NG' and id not like '%No Tol%' and id not like '%In Tol%' and id not like '%CM%' and id not like '% C\_%' ESCAPE '\\' and id not like '% C.%' and id not like '% C %' and id not like '% CC %' THEN 1 ELSE 0 END) AS NG_MM FROM CMMdata where timesave >'"+datetime_start+"' and timesave <'"+datetime_end+"' and dmc like '%"+dmc+"%' and product like '%"+product+"%' and CMMmachine like '%"+machine+"%' GROUP BY DMC,TimeStart,requester, CodePurpose,CMMCode, Line, CMMmachine, Operator, TimeSave, Product")
        cursor.execute("SELECT TimeStart, TimeSave, requester, CodePurpose, DMC, Line, CMMmachine,CMMCode, Operator, (CASE WHEN (SELECT count(value) FROM STRING_SPLIT(Product, ' ')) >= 2 THEN (SELECT dbo.ConcatValuesInColumn(Product, 2)) ELSE Product END) as Product, SUM(CASE WHEN Result != '' THEN 1 ELSE 0 END) AS Total,SUM(CASE WHEN id like '%No Tol%' THEN 1 ELSE 0 END) AS NoTol, SUM(CASE WHEN id like '%In Tol%' THEN 1 ELSE 0 END) AS InTol,SUM(CASE WHEN Result = 'OK'  and id not like '%No Tol%' and id not like '%In Tol%' THEN 1 ELSE 0 END) AS OK_Total,SUM(CASE WHEN Result = 'NG' and id not like '%No Tol%' and id not like '%In Tol%' THEN 1 ELSE 0 END) AS NG_Total,SUM(CASE WHEN Result = 'OK' and id not like '%No Tol%' and id not like '%In Tol%' and (id like '% C\_%' ESCAPE '\\' or id like '% C.%' or id like '% C %' or id like '% CC %') THEN 1 ELSE 0 END) AS OK_C,SUM(CASE WHEN Result = 'NG' and id not like '%No Tol%' and id not like '%In Tol%' and (id like '% C\_%' ESCAPE '\\' or id like '% C.%'or id like '% C %' or id like '% CC %') THEN 1 ELSE 0 END) AS NG_C,SUM(CASE WHEN Result = 'OK' and id not like '%No Tol%' and id not like '%In Tol%' and id like '%CM%' THEN 1 ELSE 0 END) AS OK_CM,SUM(CASE WHEN Result = 'NG' and id not like '%No Tol%' and id not like '%In Tol%' and id like '%CM%' THEN 1 ELSE 0 END) AS NG_CM,SUM(CASE WHEN Result = 'OK' and id not like '%No Tol%' and id not like '%In Tol%' and id not like '%CM%' and id not like '% C\_%' ESCAPE '\\' and id not like '% C.%' and id not like '% C %' and id not like '% CC %' THEN 1 ELSE 0 END) AS OK_MM,SUM(CASE WHEN Result = 'NG' and id not like '%No Tol%' and id not like '%In Tol%' and id not like '%CM%' and id not like '% C\_%' ESCAPE '\\' and id not like '% C.%' and id not like '% C %' and id not like '% CC %' THEN 1 ELSE 0 END) AS NG_MM FROM CMMdata where timesave >'"+datetime_start+"' and timesave <'"+datetime_end+"' and dmc like '%"+dmc+"%' and product like '%"+product+"%' and CMMmachine like '%"+machine+"%' GROUP BY DMC,TimeStart,requester, CodePurpose,CMMCode, Line, CMMmachine, Operator, TimeSave, Product")
        form_list = cursor.fetchall()

        # Nếu lấy dữ liệu ra trống
        if form_list == None:
            ret = {
                'status':False,
                'message':'Not Exist Data'
            }
            return jsonify(ret),400

        # Nếu all_records được truy vấn thành công
        ret = {
                'status':True,
                'message':'Success',
                'data': []
            }
        
        if len(form_list) == 0:
            ret['data'] = None                  
            return jsonify(ret)

        for item in form_list:
            time_start, time_save, requester, code_purpose, dmc, line, cmm_machine, cmm_code, operator, product_temp, total, notol, intol, ok_total, ng_total, cc_ok, cc_ng, cm_ok, cm_ng, mm_ok, mm_ng = item
            ret["data"].append({
                "timeStart": time_start,
                "timeSave": time_save,
                "requester": requester,
                "codePurpose": code_purpose,
                "dmc": dmc,
                "line": line,
                "product": product_temp,
                "cmmMachine": cmm_machine,
                "cmmCode": cmm_code,
                "operator": operator,
                "total": total,
                "noTol": notol,
                "inTol": intol,
                "ccOK": cc_ok,
                "ccNG": cc_ng,
                "cmOK": cm_ok,
                "cmNG": cm_ng,
                "mmOK": mm_ok,
                "mmNG": mm_ng
            })
        
        return jsonify(ret)
    except Exception as e:
        ret = {
            'status':False,
            'message': str(e)
        }
        Systemp_log(traceback.format_exc(), "cmm_data").append_new_line()
        return jsonify(ret),500
    
@CMM.post('/chart') 
@swag_from('./docs/CMM/chart_data.yaml')
def chart_data():
    try:
        # Tạo cusor để kết nối với database
        conn = pyodbc.connect('Driver={SQL Server}; Server=192.168.8.21; uid=sa; pwd=1234;Database=QC; Trusted_Connection=No;',timeout=1)
        cursor = conn.cursor()

        # Ngày, tên máy
        time_start = request.json['timeStart']
        time_end = request.json['timeEnd']

        cmm_machine = str(request.json["cmmMachine"]).replace('[','(').replace(']',')')

        print(time_start)
        print(time_end)
        print(cmm_machine)

        print("select timestart, timesave, cmmmachine from [QC].[dbo].[CMMdata] where cmmmachine in "+cmm_machine+" and timesave > '"+time_start+"' and timestart < '"+time_end+"' group by  timestart, timesave, cmmmachine order by cmmmachine,timesave")
        cursor.execute("select timestart, timesave, cmmmachine from [QC].[dbo].[CMMdata] where cmmmachine in "+cmm_machine+" and timesave > '"+time_start+"' and timestart < '"+time_end+"' group by  timestart, timesave, cmmmachine order by cmmmachine,timesave")
        data_list = cursor.fetchall()

        # Nếu lấy dữ liệu ra trống
        if data_list == None:
            ret = {
                'status':False,
                'message':'Not Exist Data'
            }
            return jsonify(ret),400

        # Nếu all_records được truy vấn thành công
        ret = {
                'status':True,
                'message':'Success',
                'data':[]
            }
        
        if len(data_list) == 0:
            ret['data'] = None                  
            return jsonify(ret)

        for item in data_list:
            time_start, time_save, cmm_machine = item
            ret["data"].append({
                    "x": cmm_machine,
                    "y": [int(time_start.timestamp()*1000+25200000), int(time_save.timestamp()*1000+25200000)]
                })
        
        return jsonify(ret)
    except Exception as e:
        ret = {
            'status':False,
            'message': str(e)
        }
        Systemp_log(traceback.format_exc(), "cmm_chart_data").append_new_line()
        return jsonify(ret),500
    
@CMM.get('/sixpack_products') 
@swag_from('./docs/CMM/sixpack_products.yaml')
def get_sixpack_products():
    try:
        # Tạo cusor để kết nối với database
        conn = pyodbc.connect('Driver={SQL Server}; Server=192.168.8.21; uid=sa; pwd=1234;Database=QC; Trusted_Connection=No;',timeout=1)
        cursor = conn.cursor()

        cursor.execute("select distinct(Product) as Product from CMMsixpackform  order by Product")
        sixpack_products = cursor.fetchall()

        # Nếu lấy dữ liệu ra trống
        if sixpack_products == None:
            ret = {
                'status':False,
                'message':'Not Exist Data'
            }
            return jsonify(ret),400

        # Nếu all_records được truy vấn thành công
        ret = {
                'status':True,
                'message':'Success',
                'data': []
            }
        
        if len(sixpack_products) == 0:
            ret['data'] = None                  
            return jsonify(ret)
    

        for item in sixpack_products:
            product_name = item
            ret["data"].append(product_name[0])
        
        return jsonify(ret)
    except Exception as e:
        ret = {
            'status':False,
            'message': str(e)
        }
        Systemp_log(traceback.format_exc(), "machines").append_new_line()
        return jsonify(ret),500
    
@CMM.get('/sixpack_forms/<string:dmc>') 
@swag_from('./docs/CMM/get_sixpack_forms.yaml')
def get_sixpack_form(dmc):
    try:
        # Tạo cusor để kết nối với database
        conn = pyodbc.connect('Driver={SQL Server}; Server=192.168.8.21; uid=sa; pwd=1234;Database=QC; Trusted_Connection=No;',timeout=1)
        cursor = conn.cursor()
        
        # Truy cập Database để lấy dữ liệu
        cursor.execute("select * FROM [QC].[dbo].[CMMsixpackform] where product = '"+dmc+"' order by name")
        all_data = cursor.fetchall()

        # Nếu lấy dữ liệu ra trống
        if all_data == None:
            ret = {
                'status':False,
                'message':'Not Exist Data'
            }
            return jsonify(ret),400

        # Nếu all_records được truy vấn thành công
        ret = {
                'status':True,
                'message':'Success',
                'data': []
            }
        
        if len(all_data) == 0:
            ret['data'] = None                  
            return jsonify(ret)
    

        for item in all_data: 
            product, cmm, name = item
            ret["data"].append({
                "cmm": cmm,
                "name": name
            })  

        return jsonify(ret)
    except Exception as e:
        ret = {
            'status':False,
            'message': str(e)
        }
        Systemp_log(traceback.format_exc(), "sixpack_forms").append_new_line()
        return jsonify(ret), 500
    
@CMM.get('/data/<string:dmc>/<string:datetime>')
@swag_from('./docs/CMM/data_details.yaml')
def data_details(dmc, datetime):
    try:
        # Tạo cusor để kết nối với database
        conn = pyodbc.connect('Driver={SQL Server}; Server=192.168.8.21; uid=sa; pwd=1234;Database=QC; Trusted_Connection=No;',timeout=1)
        cursor = conn.cursor()

        cursor.execute("SELECT IDx, TimeSave, Actual, Nominal, Uppertol, Lowertol, Unit, Result, Id FROM [QC].[dbo].[CMMdata] where DMC = '"+dmc+"' and TimeSave = '"+datetime+"'")
        cmm_datas = cursor.fetchall()

        # Nếu lấy dữ liệu ra trống
        if cmm_datas == None:
            ret = {
                'status':False,
                'message':'Not Exist Data'
            }
            return jsonify(ret),400

        # Nếu all_records được truy vấn thành công
        ret = {
                'status':True,
                'message':'Success',
                'data':[]
            }
        
        if len(cmm_datas) == 0:
            ret['data'] = None                  
            return jsonify(ret)
    

        for item in cmm_datas:
            idx, time_save, actual, nominal, uppertol, lowertol, unit, result, id = item
            ret["data"] += [{
            "index":idx,
            "timeSave":time_save,
            "actual":actual,
            "nominal":nominal,
            "upper":uppertol,
            "lower":lowertol,
            "unit":unit,
            "result":result,
            "name":id
        }]   
        
        return jsonify(ret)
    except Exception as e:
        ret = {
            'status':False,
            'message': str(e)
        }
        Systemp_log(traceback.format_exc(), "data_details").append_new_line()
        return jsonify(ret),500
    
@CMM.get('/form_manager') 
@swag_from('./docs/CMM/form_manager.yaml')
def get_form_manager():
    try:
        # Tạo cusor để kết nối với database
        conn = pyodbc.connect('Driver={SQL Server}; Server=192.168.8.21; uid=sa; pwd=1234;Database=QC; Trusted_Connection=No;',timeout=1)
        cursor = conn.cursor()

        cursor.execute("select distinct(FormName), FileName from CMMFormdata group by FormName, FileName")
        form_manager_list = cursor.fetchall()

        print(len(form_manager_list))

        # Nếu lấy dữ liệu ra trống
        if form_manager_list == None:
            ret = {
                'status':False,
                'message':'Not Exist Data'
            }
            return jsonify(ret),400

        # Nếu all_records được truy vấn thành công
        ret = {
                'status':True,
                'message':'Success',
                'data': []
            }
        
        if len(form_manager_list) == 0:
            ret['data'] = None                  
            return jsonify(ret)
    

        for item in form_manager_list:
            form_name, file_name = item
            ret["data"].append({
                'formName': form_name,
                'fileName': file_name
            })
        
        return jsonify(ret)
    except Exception as e:
        ret = {
            'status':False,
            'message': str(e)
        }
        Systemp_log(traceback.format_exc(), "form_manager").append_new_line()
        return jsonify(ret),500

@CMM.post('/import_data') 
@swag_from('./docs/CMM/import_data.yaml')
def test_import_file():
    try:
        conn = pyodbc.connect('Driver={SQL Server}; Server=192.168.8.21; uid=sa; pwd=1234; Database=KnifeCNCSystem; Trusted_Connection=No;',timeout=1)
        cursor = conn.cursor()

        # Kiểm tra xem 'data' có nằm trong list files không
        if 'data' not in request.files:
            ret = {
                'status':False,
                'message':'No file part'
            }
            return jsonify(ret),400

        # Lấy file storage object
        uploaded_file = request.files['data']

        # Nếu all_records được truy vấn thành công
        ret = {
                'status':True,
                'message':'Success',
                "data": []
            }
        
        # Lấy file_name
        file_name = uploaded_file.filename

        # Lấy tên máy
        if len(file_name.split('OP')) == 2:
            machine_name = file_name.split('OP')[1].split('-')[1].split('.')[0]
        else:
            machine_name = file_name.split('OP')[2].split('-')[1].split('.')[0]

        # Xóa toàn bộ dữ liệu bảng Bom với Machine_Name là machine_name phía trên
        cursor.execute("delete from Bom where Machine_Name = '"+machine_name+"'")
        conn.commit()

        # Lấy danh sách các sheet
        xls_sheetnames = pd.ExcelFile(uploaded_file).sheet_names

        # Duyệt qua danh sách các sheetname rồi lấy dữ liệu của từng sheetname
        for sheetname in xls_sheetnames:
            sheet_data = pd.read_excel(uploaded_file, sheet_name=sheetname)
            
            # lấy op
            op = sheetname
            
            print(sheet_data.head())

            # lấy dmc_product
            dmc_product_text = sheet_data.at[2, "TIÊU CHUẨN DAO CỤ\nTHE STANDARD OF TOOL USEAGE"]
            dmc_product = dmc_product_text.split(":")[1].strip()[:7]

            # duyệt qua từng dòng của dataframe để lấy dữ liệu
            for idx, row in sheet_data.iterrows():
                if isinstance(row[0], int):
                    print(row)
                    print("row[0]", row[0])
                    
                    # Lấy tool_holder
                    tool_holder = row[1]

                    if tool_holder is None:
                        break
                    elif tool_holder == 'N/A':
                        tool_holder = '0'
                    else:
                        tool_holder = tool_holder.split('T')[1]
                        if '(' in tool_holder:
                            tool_holder = tool_holder.split('(')[0]

                    # Lấy tool_type và arbor_type
                    tool_type = row[3]
                    arbor_type = row[7].replace("\n", "").strip()

                    # Lấy tool_useage
                    tool_useage_to_check = row[12]
                    
                    if isinstance(tool_useage_to_check, int):
                        tool_useage = tool_useage_to_check
                    else:
                        if len(tool_useage_to_check.split(":")) > 1:
                            if len(tool_useage_to_check.split(":")) == 2:
                                if ')' in tool_useage_to_check.split(":")[1]:
                                    tool_useage = tool_useage_to_check.split(":")[1].replace(')', '')
                                else:
                                    tool_useage = tool_useage_to_check.split(":")[1]
                            elif len(tool_useage_to_check.split(":")) == 3:
                                if ":" in tool_useage_to_check.split()[2]:
                                    tool_useage = tool_useage_to_check.split()[2][1:]
                                else:
                                    tool_useage = tool_useage_to_check.split()[2]
                            else:
                                if 'PCS' in tool_useage_to_check.split(":")[1].split("\n")[0].strip():
                                    tool_useage = tool_useage_to_check.split(":")[1].split("\n")[0].strip().replace(' PCS', '')
                                else:
                                    tool_useage = tool_useage_to_check.split(":")[1].split("\n")[0].strip()
                        else:
                            tool_useage = 0

                    # Lấy diameter và tolerance
                    diameter_tolerance = row[15]
                    diameter_tolerance = diameter_tolerance.split('+')

                    diameter = diameter_tolerance[0]
                    tolerance = diameter_tolerance[1]
                
                    print((machine_name, dmc_product, op, tool_type, tool_holder, arbor_type, tool_useage, diameter, tolerance))
                
                    cursor.execute( 
                            '''INSERT INTO Bom VALUES (?,?,?,?,?,?,?,?,?) ''',
                                machine_name,
                                dmc_product,
                                op,
                                tool_type, 
                                tool_holder,
                                arbor_type, 
                                tool_useage,
                                diameter,
                                tolerance
                        )
                    cursor.commit()

        cursor.execute("select * FROM [KnifeCNCSystem].[dbo].[Bom]")
        all_records = cursor.fetchall()
        conn.close()
        
        for item in all_records:
            idx, machine_name, dmc_product, op, tool_type, tool_holder, arbor_type, tool_useage, diameter, tolerance = item
            ret['data'].append({
                'machine_name':machine_name.strip(),
                'dmc_product':dmc_product.strip(),
                'op':op.strip(),
                'tool_type':tool_type.strip(),
                'tool_holder':tool_holder,
                'arbor_type':arbor_type.strip(),
                'tool_usage':tool_useage,
                'diameter':diameter,
                'tolerance':tolerance
            })
            
        return jsonify(ret)
    except Exception as e:
        ret = {
            'status':False,
            'message': str(e)
        }
        Systemp_log(traceback.format_exc(), "form_manager").append_new_line()
        return jsonify(ret),500
    
@CMM.get('/form_manager/<string:form_name>') 
@swag_from('./docs/CMM/form_manager_detail.yaml')
def get_form_manager_detail(form_name):
    try:
        # Tạo cusor để kết nối với database
        conn = pyodbc.connect('Driver={SQL Server}; Server=192.168.8.21; uid=sa; pwd=1234;Database=QC; Trusted_Connection=No;',timeout=1)
        cursor = conn.cursor()

        cursor.execute("SELECT Position, CircleNum, Characteristic, Link FROM [QC].[dbo].[CMMFormdata] where FormName = '"+form_name+"'")
        form_manager_list = cursor.fetchall()

        print(len(form_manager_list))

        # Nếu lấy dữ liệu ra trống
        if form_manager_list == None:
            ret = {
                'status':False,
                'message':'Not Exist Data'
            }
            return jsonify(ret),400

        # Nếu all_records được truy vấn thành công
        ret = {
                'status':True,
                'message':'Success',
                'data': []
            }
        
        if len(form_manager_list) == 0:
            ret['data'] = None                  
            return jsonify(ret)
    

        for item in form_manager_list:
            position, circleNum, characteristic, link = item
            ret["data"] += [{
                "position":position,
                "circleNum":circleNum,
                "characteristic":characteristic,
                "link":link
            }]
        
        return jsonify(ret)
    except Exception as e:
        ret = {
            'status':False,
            'message': str(e)
        }
        Systemp_log(traceback.format_exc(), "form_manager").append_new_line()
        return jsonify(ret),500
    
@CMM.get('/dmc_data/<string:dmc>') 
@swag_from('./docs/CMM/dmc_data.yaml')
def get_dmc_data(dmc):
    try:
        # Tạo cusor để kết nối với database
        conn = pyodbc.connect('Driver={SQL Server}; Server=192.168.8.21; uid=sa; pwd=1234;Database=QC; Trusted_Connection=No;',timeout=1)
        cursor = conn.cursor()

        if dmc =="":
            dmc= "datnon"

        cursor.execute("SELECT id,actual FROM [QC].[dbo].[CMMdata] where DMC like '%"+dmc+"%' order by IDx")
        dmc_data_list = cursor.fetchall()

        print(len(dmc_data_list))

        # Nếu lấy dữ liệu ra trống
        if dmc_data_list == None:
            ret = {
                'status':False,
                'message':'Not Exist Data'
            }
            return jsonify(ret),400

        # Nếu all_records được truy vấn thành công
        ret = {
                'status':True,
                'message':'Success',
                'data': []
            }
        
        if len(dmc_data_list) == 0:
            ret['data'] = None                  
            return jsonify(ret)
    

        for idx, item in enumerate(dmc_data_list):
            id, actual = item
            ret["data"] += [{
                "id":id,
                "actual":actual
            }]
        
        return jsonify(ret)
    except Exception as e:
        ret = {
            'status':False,
            'message': str(e)
        }
        Systemp_log(traceback.format_exc(), "dmc_data").append_new_line()
        return jsonify(ret),500