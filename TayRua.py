from os import access
# from constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
from constants.http_status_code import HTTP_201_CREATED
# from flask import Blueprint, app, request, jsonify
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flasgger import swag_from
from database import *
from ERROR import *
import datetime
from threading import Thread

TayRua = Blueprint("TayRua", __name__, url_prefix="/api/v1/TayRua")

# Thêm lịch sử sử dụng máy mỗi lần quét máy (Cũng áp dụng cho cả Biavia lẫn tẩy rửa) => KHÔNG CẦN LÀM LẠI

# Thêm từng con hàng vào bảng TayRua_Product
@TayRua.post('/Insert_Tayrua_Products')
@swag_from('./docs/Tayrua/Insert_Tayrua_Products.yaml')
def Insert_Tayrua_Products():
    try:
        Tayrua_Machine = request.json['Tayrua_Machine']
        Product_Code = request.json['Product_Code']
        Product_Type = request.json['Product_Type']
        print("INSERT INTO [BonusCalculation].[dbo].[TayRua_Products](Tayrua_MC, Product_Code, Product_Type, TimeSave)"
            " VALUES ('" + Tayrua_Machine + "','" + Product_Code + "', '" + Product_Type + "', '" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "')")
        cursor.execute("INSERT INTO [BonusCalculation].[dbo].[TayRua_Products](Tayrua_MC, Product_Code, Product_Type, TimeSave)"
            " VALUES ('" + Tayrua_Machine + "','" + Product_Code + "', '" + Product_Type + "', '" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "')")
        conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Insert_Tayrua_Products").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify('OK'), HTTP_201_CREATED

# Tính sản lượng Tẩy Rửa
@TayRua.get('/Calculate_Tayrua_Productivity_Today')
@swag_from('./docs/Tayrua/Calculate_Tayrua_Productivity_Today.yaml')
def Calculate_Tayrua_Productivity_Today():
    try:
        Worker_Code = request.json['Worker_Code']

        # Thưc thi câu lệnh
        print("with x as (select DISTINCT a.Machine, a.Worker_Code, a1.Worker_Name, a.TimeIn from [BonusCalculation].[dbo].[Machine_History] a, [BonusCalculation].[dbo].[Worker_Manager] a1 where a.Worker_Code = a1.Worker_Code and a.Status = 1 and DATEDIFF(MINUTE, a.TimeIn, GETDATE()) > 0 and DATEDIFF(MINUTE, a.TimeIn, GETDATE()) < 720) select DISTINCT x.Machine, x.Worker_Name, b.Process, c.COM from x, [BonusCalculation].[dbo].[Machine_CNC] b, [BonusCalculation].[dbo].[Machine_COM] c where x.Machine = b.OP1 and b.Process = N'Tẩy rửa' and DATEDIFF(MINUTE, x.TimeIn, GETDATE()) > 0 and DATEDIFF(MINUTE, x.TimeIn, GETDATE()) < 720 and b.OP1 = c.Machine_Code")
        cursor.execute("with x as (select DISTINCT a.Machine, a.Worker_Code, a1.Worker_Name, a.TimeIn from [BonusCalculation].[dbo].[Machine_History] a, [BonusCalculation].[dbo].[Worker_Manager] a1 where a.Worker_Code = a1.Worker_Code and a.Status = 1 and DATEDIFF(MINUTE, a.TimeIn, GETDATE()) > 0 and DATEDIFF(MINUTE, a.TimeIn, GETDATE()) < 720) select DISTINCT x.Machine, x.Worker_Name, b.Process, c.COM from x, [BonusCalculation].[dbo].[Machine_CNC] b, [BonusCalculation].[dbo].[Machine_COM] c where x.Machine = b.OP1 and b.Process = N'Tẩy rửa' and DATEDIFF(MINUTE, x.TimeIn, GETDATE()) > 0 and DATEDIFF(MINUTE, x.TimeIn, GETDATE()) < 720 and b.OP1 = c.Machine_Code")
        
        # Cập nhật sự thay đổi của table
        cursor.commit()
    except Exception as e:
        Systemp_log(str(e), "Calculate_Tayrua_Productivity_Today").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"), HTTP_201_CREATED

@TayRua.post('/Get_Tayrua_Worker_Infor_Today')
@swag_from('./docs/Tayrua/Get_Tayrua_Worker_Infor_Today.yaml')
def Get_Tayrua_Worker_Infor_Today():
    try:
        # Thưc thi câu lệnh
        print("  with x as (select DISTINCT a.Machine, a.Worker_Code, a1.Worker_Name, a.TimeIn from [BonusCalculation].[dbo].[Machine_History] a, [BonusCalculation].[dbo].[Worker_Manager] a1 where a.Worker_Code = a1.Worker_Code and a.Status = 1 and DATEDIFF(MINUTE, a.TimeIn, GETDATE()) > 0 and DATEDIFF(MINUTE, a.TimeIn, GETDATE()) < 720) select DISTINCT x.Machine, x.Worker_Name, b.Process, c.COM from x, [BonusCalculation].[dbo].[Machine_CNC] b, [BonusCalculation].[dbo].[Machine_COM] c where x.Machine = b.OP1 and b.Process = N'Tẩy Rửa' and DATEDIFF(MINUTE, x.TimeIn, GETDATE()) > 0 and DATEDIFF(MINUTE, x.TimeIn, GETDATE()) < 720 and b.OP1 = c.Machine_Code")
        cursor.execute("  with x as (select DISTINCT a.Machine, a.Worker_Code, a1.Worker_Name, a.TimeIn from [BonusCalculation].[dbo].[Machine_History] a, [BonusCalculation].[dbo].[Worker_Manager] a1 where a.Worker_Code = a1.Worker_Code and a.Status = 1) select DISTINCT x.Machine, x.Worker_Name, b.Process, c.COM from x, [BonusCalculation].[dbo].[Machine_CNC] b, [BonusCalculation].[dbo].[Machine_COM] c where x.Machine = b.OP1 and b.Process = N'Tẩy Rửa' and b.OP1 = c.Machine_Code")
        result = cursor.fetchall()

        print(result)
        # Đưa result về dạng json
        json_result = {}
        for idx in range(len(result)):
            json_result[result[idx][0]] = [result[idx][1], result[idx][2], result[idx][3].strip()]

        print(json_result)

        # Cập nhật sự thay đổi của table
        cursor.commit()
    except Exception as e:
        Systemp_log(str(e), "Get_Tayrua_Worker_Infor_Today").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify(json_result), HTTP_201_CREATED

@TayRua.post('/Get_Tayrua_Productivity_Today_By_Tayrua_Code')
@swag_from('./docs/Tayrua/Get_Tayrua_Productivity_Today_By_Tayrua_Code.yaml')
def Get_Tayrua_Productivity_Today_By_Tayrua_Code():
    try:
        # Thưc thi câu lệnh
        print("with x as (select * from [BonusCalculation].[dbo].[TayRua_Products] a, [BonusCalculation].[dbo].[Machine_History] b where a.Tayrua_MC = b.Machine and DATEDIFF(MINUTE, b.TimeIn, GETDATE()) > 0 and DATEDIFF(MINUTE, b.TimeIn, GETDATE()) < 720) select x.Tayrua_MC, sum(case when x.TimeOut IS NULL and x.Status = 1 and DATEDIFF(MINUTE, x.TimeIn, x.TimeSave) > 0 and DATEDIFF(MINUTE, x.TimeIn, x.TimeSave) < 720 THEN 1 else 0 end) as SanLuong from x group by x.Tayrua_MC")
        cursor.execute("with x as (select * from [BonusCalculation].[dbo].[TayRua_Products] a, [BonusCalculation].[dbo].[Machine_History] b where a.Tayrua_MC = b.Machine and DATEDIFF(MINUTE, b.TimeIn, GETDATE()) > 0 and DATEDIFF(MINUTE, b.TimeIn, GETDATE()) < 720) select x.Tayrua_MC, sum(case when x.TimeOut IS NULL and x.Status = 1 and DATEDIFF(MINUTE, x.TimeIn, x.TimeSave) > 0 and DATEDIFF(MINUTE, x.TimeIn, x.TimeSave) < 720 THEN 1 else 0 end) as SanLuong from x group by x.Tayrua_MC")
        result = cursor.fetchall()

        # Đưa result về dạng json
        json_result = {}
        for idx in range(len(result)):
            json_result[result[idx][0]] = result[idx][1]

        print(json_result)
        # Cập nhật sự thay đổi của table
        cursor.commit()
    except Exception as e:
        Systemp_log(str(e), "Get_Tayrua_Productivity_Today_By_Tayrua_Code").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify(json_result), HTTP_201_CREATED

@TayRua.post('/Get_Distinct_Tayrua_Productivity_Today_Realtime_By_Tayrua_Code')
@swag_from('./docs/Tayrua/Get_Distinct_Tayrua_Productivity_Today_Realtime_By_Tayrua_Code.yaml')
def Get_Distinct_Bavia_Productivity_Today_Realtime_By_Bavia_Code():
    try:
        # Thưc thi câu lệnh
        print("  with x as (select * from [BonusCalculation].[dbo].[TayRua_Products] a, [BonusCalculation].[dbo].[Machine_History] b where a.Tayrua_MC = b.Machine and DATEDIFF(MINUTE, b.TimeIn, GETDATE()) > 0 and DATEDIFF(MINUTE, b.TimeIn, GETDATE()) < 720) select x.Tayrua_MC, count (DISTINCT x.Product_Code) from x where x.TimeOut IS NULL and x.Status = 1 and DATEDIFF(MINUTE, x.TimeIn, x.TimeSave) > 0 and DATEDIFF(MINUTE, x.TimeIn, x.TimeSave) < 720 group by x.Tayrua_MC")
        cursor.execute("  with x as (select * from [BonusCalculation].[dbo].[TayRua_Products] a, [BonusCalculation].[dbo].[Machine_History] b where a.Tayrua_MC = b.Machine and DATEDIFF(MINUTE, b.TimeIn, GETDATE()) > 0 and DATEDIFF(MINUTE, b.TimeIn, GETDATE()) < 720) select x.Tayrua_MC, count (DISTINCT x.Product_Code) from x where x.TimeOut IS NULL and x.Status = 1 and DATEDIFF(MINUTE, x.TimeIn, x.TimeSave) > 0 and DATEDIFF(MINUTE, x.TimeIn, x.TimeSave) < 720 group by x.Tayrua_MC")
        result = cursor.fetchall()

        # Đưa result về dạng json
        json_result = {}
        for idx in range(len(result)):
            json_result[result[idx][0]] = result[idx][1]

        print(json_result)
        # Cập nhật sự thay đổi của table
        cursor.commit()
    except Exception as e:
        Systemp_log(str(e), "Get_Distinct_Tayrua_Productivity_Today_Realtime_By_Tayrua_Code").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify(json_result), HTTP_201_CREATED
