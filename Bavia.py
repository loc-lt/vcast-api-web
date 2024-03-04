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

Bavia = Blueprint("Bavia", __name__, url_prefix="/api/v1/Bavia")

# # Thêm lịch sử sử dụng bàn Bavia mỗi lần quét (chưa có TimeOut, đổi Status thành 1) - BỎ VÌ KHÔNG CẦN THIẾT => SỬ DỤNG Machine_Historys + Machine_Register
# @Bavia.post('/Insert_Bavia_History')
# @swag_from('./docs/Bavia/Insert_Bavia_History.yaml')
# def Insert_Bavia_History():
#     try:
#         Worker_Code = request.json['Worker_Code']
#         Bavia = request.json['Bavia']
#         Quantity = request.json['Quantity']
#         print("INSERT INTO [BonusCalculation].[dbo].[Bavia_History](Worker_Code, Bavia, TimeIn, Quantity, Date, Status)"
#             " VALUES ('" + Worker_Code + "','" + Bavia + "', '" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "', '" + Quantity + "', CONVERT(Date, '" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "'), '" + "1" + "')")
#         cursor.execute("INSERT INTO [BonusCalculation].[dbo].[Bavia_History](Worker_Code, Bavia, TimeIn, Quantity, Date, Status)"
#             " VALUES ('" + Worker_Code + "','" + Bavia + "', '" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "', '" + Quantity + "', CONVERT(Date, '" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "'), '" + "1" + "')")
#         conn.commit()
#     except Exception as e:
#         Systemp_log(str(e), "Insert_Bavia_History").append_new_line()
#         return jsonify({"Error": "Invalid request, please try again."})
#     return jsonify('OK'), HTTP_201_CREATED

# Thêm từng con hàng vào bảng Bavia_Products mỗi lần quét qua
@Bavia.post('/Insert_Bavia_Products')
@swag_from('./docs/Bavia/Insert_Bavia_Products.yaml')
def Insert_Bavia_Products():
    try:
        Bavia_Code = request.json['Bavia_Code']
        Product_Code = request.json['Product_Code']
        Product_Type = request.json['Product_Type']
        print("INSERT INTO [BonusCalculation].[dbo].[Bavia_Products](Bavia_Code, Product_Code, Product_Type, TimeSave)"
            " VALUES ('" + Bavia_Code + "','" + Product_Code + "', '" + Product_Type + "', '" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "')")
        cursor.execute("INSERT INTO [BonusCalculation].[dbo].[Bavia_Products](Bavia_Code, Product_Code, Product_Type, TimeSave)"
            " VALUES ('" + Bavia_Code + "','" + Product_Code + "', '" + Product_Type + "', '" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "')")
        conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Insert_Bavia_Products").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify('OK'), HTTP_201_CREATED

# Tính sản lượng Bavia
@Bavia.get('/Calculate_Bavia_Productivity_Today')
@swag_from('./docs/Bavia/Calculate_Bavia_Productivity_Today.yaml')
def Calculate_Bavia_Productivity_Today():
    try:
        Worker_Code = request.json['Worker_Code']

        # Thưc thi câu lệnh
        print("with x as (select a.Worker_Code, c.Stage, c.Line_Code, Count(*) as Productivity from Machine_History a, Bavia_Products b, Machine_Register c where a.Machine = b.Bavia_Code and b.Bavia_Code = c.Machine_Code and a.Worker_Code = c.Worker and DATEDIFF(hour, b.TimeSave, GETDATE()) < 12 and a.Worker_Code = '"+ Worker_Code+"' group by a.Worker_Code, c.Stage, c.Line_Code having c.Stage = 'Bavia') select x.*, case when count(Line_Code) = 6 and sum(Productivity) >= 270 and Productivity >= 45 then Productivity * 230 when count(Line_Code) = 7 and sum(Productivity) >= 315 and Productivity >= 45 then Productivity * 345 when count(Line_Code) = 8 and sum(Productivity) >= 360 and Productivity >= 45 then Productivity * 414 else 0 end as MoneyBouns from x group by x.Worker_Code, x.Stage, x.Line_Code, x.Productivity")
        cursor.execute("with x as (select a.Worker_Code, c.Stage, c.Line_Code, Count(*) as Productivity from Machine_History a, Bavia_Products b, Machine_Register c where a.Machine = b.Bavia_Code and b.Bavia_Code = c.Machine_Code and a.Worker_Code = c.Worker and DATEDIFF(hour, b.TimeSave, GETDATE()) < 12 and a.Worker_Code = '"+ Worker_Code+"' group by a.Worker_Code, c.Stage, c.Line_Code having c.Stage = 'Bavia') select x.*, case when count(Line_Code) = 6 and sum(Productivity) >= 270 and Productivity >= 45 then Productivity * 230 when count(Line_Code) = 7 and sum(Productivity) >= 315 and Productivity >= 45 then Productivity * 345 when count(Line_Code) = 8 and sum(Productivity) >= 360 and Productivity >= 45 then Productivity * 414 else 0 end as MoneyBouns from x group by x.Worker_Code, x.Stage, x.Line_Code, x.Productivity")
        
        # Cập nhật sự thay đổi của table
        cursor.commit()
    except Exception as e:
        Systemp_log(str(e), "Calculate_Bavia_Productivity_Today").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"), HTTP_201_CREATED

@Bavia.post('/Get_Bavia_Worker_Infor_Today')
@swag_from('./docs/Bavia/Get_Bavia_Worker_Infor_Today.yaml')
def Get_Bavia_Worker_Infor_Today():
    try:
        # Thưc thi câu lệnh
        print("with x as (select * from [BonusCalculation].[dbo].[Bavia_Products] a, [BonusCalculation].[dbo].[Machine_History] b where a.Bavia_Code = b.Machine and DATEDIFF(SECOND, b.TimeIn, GETDATE()) > 0 and DATEDIFF(MINUTE, b.TimeIn, GETDATE()) < 720) select x.Bavia_Code, count (DISTINCT x.Product_Code) from x where x.TimeOut IS NULL and x.Status = 1 and DATEDIFF(SECOND, x.TimeIn, x.TimeSave) > 0 and DATEDIFF(MINUTE, x.TimeIn, x.TimeSave) < 720 group by x.Bavia_Code")
        cursor.execute("with x as (select DISTINCT a.Machine, a.Worker_Code, a1.Worker_Name, a.TimeIn from [BonusCalculation].[dbo].[Machine_History] a, [BonusCalculation].[dbo].[Worker_Manager] a1 where a.Worker_Code = a1.Worker_Code and a.Status = 1) select DISTINCT x.Machine, x.Worker_Name, b.Process, c.COM from x, [BonusCalculation].[dbo].[Machine_CNC] b, [BonusCalculation].[dbo].[Machine_COM] c where x.Machine = b.OP1 and b.Process = 'Bavia' and b.OP1 = c.Machine_Code")
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
        Systemp_log(str(e), "Get_Bavia_Worker_Infor_Today").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify(json_result), HTTP_201_CREATED

@Bavia.post('/Get_Bavia_Productivity_Today_Realtime_By_Bavia_Code')
@swag_from('./docs/Bavia/Get_Bavia_Productivity_Today_Realtime_By_Bavia_Code.yaml')
def Get_Bavia_Productivity_Today_Realtime_By_Bavia_Code():
    try:
        # Thưc thi câu lệnh
        print("with x as (select * from [BonusCalculation].[dbo].[Bavia_Products] a, [BonusCalculation].[dbo].[Machine_History] b where a.Bavia_Code = b.Machine and DATEDIFF(MINUTE, b.TimeIn, GETDATE()) > 0 and DATEDIFF(MINUTE, b.TimeIn, GETDATE()) < 720) select x.Bavia_Code, sum(case when x.TimeOut IS NULL and x.Status = 1 and DATEDIFF(MINUTE, x.TimeIn, x.TimeSave) > 0 and DATEDIFF(MINUTE, x.TimeIn, x.TimeSave) < 720 THEN 1 else 0 end) as SanLuong from x group by x.Bavia_Code")
        cursor.execute("with x as (select a.Bavia_Code, b.TimeIn, b.TimeOut, a.Product_Code, a.TimeSave from [BonusCalculation].[dbo].[Bavia_Products] a inner join [BonusCalculation].[dbo].[Machine_History] b on a.Bavia_Code = b.Machine), y as (select * from [BonusCalculation].[dbo].[laythoigian]()), z as (select x.Bavia_Code, x.TimeIn, x.TimeOut, x.Product_Code, count(DISTINCT x.TimeSave) AS SL from x, y where (DATEDIFF(SECOND, x.TimeIn, x.TimeSave) > 0 and DATEDIFF(MINUTE, x.TimeIn, x.TimeSave) < 720 and DATEDIFF(SECOND, x.TimeSave, x.TimeOut) > 0 and DATEDIFF(MINUTE, x.TimeSave, x.TimeOut) < 720 and DATEDIFF(SECOND, y.TimeIn, x.Timein) > 0 and DATEDIFF(MINUTE, y.TimeIn, x.TimeOut) < 720) or (x.TimeOut IS NULL and DATEDIFF(SECOND, x.TimeIn, x.TimeSave) > 0) group by x.Bavia_Code, x.TimeIn, x.TimeOut, x.Product_Code) select z.Bavia_Code, sum(z.SL) from z group by z.Bavia_Code;")
        result = cursor.fetchall()

        # Đưa result về dạng json
        json_result = {}
        for idx in range(len(result)):
            json_result[result[idx][0]] = result[idx][1]

        print(json_result)
        # Cập nhật sự thay đổi của table
        cursor.commit()
    except Exception as e:
        Systemp_log(str(e), "Get_Bavia_Productivity_Today_Realtime_By_Bavia_Code").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify(json_result), HTTP_201_CREATED

@Bavia.post('/Get_Distinct_Bavia_Productivity_Today_Realtime_By_Bavia_Code')
@swag_from('./docs/Bavia/Get_Distinct_Bavia_Productivity_Today_Realtime_By_Bavia_Code.yaml')
def Get_Distinct_Bavia_Productivity_Today_Realtime_By_Bavia_Code():
    try:
        # Thưc thi câu lệnh
        print("with x as (select * from [BonusCalculation].[dbo].[Bavia_Products] a, [BonusCalculation].[dbo].[Machine_History] b where a.Bavia_Code = b.Machine and DATEDIFF(MINUTE, b.TimeIn, GETDATE()) > 0 and DATEDIFF(MINUTE, b.TimeIn, GETDATE()) < 720) select x.Bavia_Code, count (DISTINCT x.Product_Code) from x where x.TimeOut IS NULL and x.Status = 1 and DATEDIFF(MINUTE, x.TimeIn, x.TimeSave) > 0 and DATEDIFF(MINUTE, x.TimeIn, x.TimeSave) < 720 group by x.Bavia_Code")
        cursor.execute("with x as (select * from [BonusCalculation].[dbo].[Bavia_Products] a, [BonusCalculation].[dbo].[Machine_History] b where a.Bavia_Code = b.Machine), y as (select * from [BonusCalculation].[dbo].[laythoigian]()) select x.Bavia_Code, count (DISTINCT x.Product_Code) from x, y where DATEDIFF(MINUTE, y.TimeIn, x.TimeSave) > 0 and DATEDIFF(MINUTE, y.TimeIn, x.TimeSave) < 730 group by x.Bavia_Code")
        result = cursor.fetchall()

        # Đưa result về dạng json
        json_result = {}
        for idx in range(len(result)):
            json_result[result[idx][0]] = result[idx][1]

        print(json_result)
        # Cập nhật sự thay đổi của table
        cursor.commit()
    except Exception as e:
        Systemp_log(str(e), "Get_Distinct_Bavia_Productivity_Today_Realtime_By_Bavia_Code").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify(json_result), HTTP_201_CREATED
