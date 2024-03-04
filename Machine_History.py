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

Machine_History = Blueprint("Machine_History", __name__, url_prefix="/api/v1/Machine_History")

# Thêm lịch sử sử dụng máy mỗi lần quét máy (chưa có TimeOut, đổi Status thành 1) 
@Machine_History.post('/Insert_Data_Machine_History')
@swag_from('./docs/Machine_History/Insert_Data_Machine_History.yaml')
def Insert_Machine_History():
    try:
        # MCHistory_id = request.json['MCHistory_id']
        Worker_Code = request.json['Worker_Code']
        Machine = request.json['Machine']
        # TimeIn = request.json['TimeIn']
        # TimeOut = request.json['TimeOut']
        Quantity = request.json['Quantity'] # Số lượng hiện chạy đc của máy này
        # Date = request.json['Date']
        Status = request.json['Status']
        # print("IF (SELECT TOP (1) [TimeOut] FROM [BonusCalculation].[dbo].[Machine_History] where Machine = '" + Machine +"' order by TimeIn desc) IS NOT NULL BEGIN INSERT INTO [BonusCalculation].[dbo].[Machine_History](Worker_Code, Machine, TimeIn, Quantity, Date, Status) VALUES ('" + Worker_Code + "','" + Machine + "', '" + TimeIn + "', '" + Quantity + "', CONVERT(Date, '" + TimeIn + "'), '" + Status + "') END ELSE PRINT N'Máy này hiện đang có người khác đảm nhiệm!'")
        cursor.execute("IF (SELECT TOP (1) [TimeOut] FROM [BonusCalculation].[dbo].[Machine_History] where Machine = '" + Machine +"' order by TimeIn desc) IS NOT NULL OR (SELECT COUNT(*) FROM [BonusCalculation].[dbo].[Machine_History] where Machine = '" + Machine + "') = 0 BEGIN INSERT INTO [BonusCalculation].[dbo].[Machine_History](Worker_Code, Machine, TimeIn, Quantity, Date, Status) VALUES ('" + Worker_Code + "','" + Machine + "', CONVERT(NVARCHAR(19), GETDATE(), 120), '" + Quantity + "', CONVERT(Date, getdate()), '" + Status + "') END ELSE PRINT N'Máy này hiện đang có người khác đảm nhiệm!'")
        conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Insert_Data_Machine_History").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify('OK'), HTTP_201_CREATED

# Cập nhật lại Status khi công nhân đăng xuất, cập nhật Quantity sau khi hoàn thành 1 con hàng - LÀM SAU, cập nhật TimeOut khi lại máy quản lý xác nhận máy đã tắt
@Machine_History.post('/Update_Data_Machine_History')
@swag_from('./docs/Machine_History/Update_Data_Machine_History.yaml')
def Update_Machine_History():
    try:
        # Các thuộc tính cần thiết để biết record nào cần update
        # Date = request.json['Date']
        Worker_Code = request.json['Worker_Code']
        TimeIn = request.json['TimeIn']
        Line_No = request.json['Line_No']
        

        # Các thuộc tính cần update
        Status = request.json['Status']

        # Thưc thi câu lệnh
        print("Update  [BonusCalculation].[dbo].[Machine_History] set TimeOut ='"+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"',Quantity = (select ISNULL(Qty1*2, 0) as Qty1 from [BonusCalculation].[dbo].[sanluongthoatmay]('" +TimeIn+"',getdate()) where Line_no ='"+Line_No+"' and TimeIn ='"+TimeIn+"' and Worker_code = '"+Worker_Code+"'), Status = '"+ Status +"' where Worker_Code ='"+Worker_Code+"'  and Timein = '"+TimeIn+"'")
        cursor.execute("Update [BonusCalculation].[dbo].[Machine_History] set TimeOut ='"+datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"',Quantity = (select ISNULL(Qty1*2, 0) as Qty1 from [BonusCalculation].[dbo].[sanluongthoatmay]('" +TimeIn+"',getdate(),'" +Worker_Code+"') where Line_no ='"+Line_No+"' and TimeIn ='"+TimeIn+"' and Worker_code = '"+Worker_Code+"'), Status = '"+ Status +"' where Worker_Code ='"+Worker_Code+"'  and Timein = '"+TimeIn+"'")
        
        # Cập nhật sự thay đổi của table
        cursor.commit()
    except Exception as e:
        Systemp_log(str(e), "Update_Machine_History").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"), HTTP_201_CREATED

# Tính sản lượng theo ngày
@Machine_History.post('/Insert_Quantity_Daily')
@swag_from('./docs/Machine_History/Insert_Quantity_Daily.yaml')
def Insert_Quantity_Daily():
    try:
        # Các thuộc tính cần thiết để insert
        Worker_Code = request.json['Worker_Code']
        Process = request.json['Process']
        Line_No = request.json['Line_No']
        Date = request.json['Date']
        Quantity = request.json['Quantity']
        NG = request.json['NG']
        Bonus = request.json['Bonus']
        Function_Code = request.json['Function_Code']

        # Thưc thi câu lệnh
        print("INSERT INTO [BonusCalculation].[dbo].[Quantity_Daily](Worker_Code, Process, Line_No, Date, Quantity, NG, Bonus,Function_Code)"
            " VALUES ('" + Worker_Code + "', N'" + Process + "', '" + Line_No + "', '" + Date + "', '" + str(Quantity) + "', '" + str(NG) + "', '" + str(Bonus) + "','" + str(Function_Code) + "')")
        cursor.execute("INSERT INTO [BonusCalculation].[dbo].[Quantity_Daily](Worker_Code, Process, Line_No, Date, Quantity, NG, Bonus,Function_Code)"
            " VALUES ('" + Worker_Code + "', N'" + Process + "', '" + Line_No + "', '" + Date + "', '" + str(Quantity) + "', '" + str(NG) + "', '" + str(Bonus) + "','" + str(Function_Code) + "')")
        
        # Cập nhật sự thay đổi của table
        cursor.commit()
    except Exception as e:
        Systemp_log(str(e), "Insert_Quantity_Daily").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"), HTTP_201_CREATED

@Machine_History.get('/Get_Quantity_Manager')
@swag_from('./docs/Machine_History/Get_Quantity_Manager.yaml')
def Get_Quantity_Manager():
    try:
        # Product_Code = request.json['Product_Code']

        cursor.execute("select [Worker_Code],[Machine_CNC].[Line_no],[Machine],[Machine_CNC].Function_Code,[TimeIn],[TimeOut] from [BonusCalculation].[dbo].[Machine_History] left join [BonusCalculation].[dbo].[Machine_CNC] on ([Machine_History].Machine = Machine_CNC.OP1 or [Machine_History].Machine = Machine_CNC.OP2) where [Status] = '1' group by [Worker_Code],[Machine_CNC].[Line_no],[Machine],[TimeIn],[TimeOut],[Machine_CNC].Function_Code")
        
        # Fetch all rows
        rows = cursor.fetchall()

        result_dict = {'data':[]}  # Dict to store the final result
        print(result_dict)

        for row in rows:    
            # Extract values from the row
            Worker_Code, Line_no, Machine, Function_Code, TimeIn, TimeOut = row

            # Create a dictionary for the current row
            current_row_dict = {
                "Worker_Code": Worker_Code,
                "Line_no": Line_no,
                "Machine": Machine,
                "Function_Code": Function_Code,
                "TimeIn": TimeIn,
                "TimeOut": TimeOut
            }

            # Add the current row dictionary to the result dictionary
            result_dict['data'].append(current_row_dict)
        print(result_dict)

        return jsonify(result_dict), HTTP_201_CREATED
    except Exception as e:
        Systemp_log(str(e), "Get_Quantity_Manager").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})

@Machine_History.post('/Get_Quantity_Op')
@swag_from('./docs/Machine_History/Get_Quantity_Op.yaml')
def Get_Quantity_Op():
    try:
        timein = request.json['timein']
        timeout = request.json['timeout']
        manv = request.json['manv']
        line = request.json['line']
        cursor.execute("select SL.Worker_code, SL.Line_no,Worker_Manager.Worker_name, ISNULL(Qty1*2, 0) AS Qty1 from [BonusCalculation].[dbo].[sanluongtheongay8]('"+timein+"','"+timeout+"','"+manv+"' ) as SL left join [BonusCalculation].[dbo].[Worker_Manager] on SL.Worker_code = Worker_Manager.Worker_code   where SL.Worker_code = '"+manv+"' and Line_no ='"+line+"'  order by Machineno, SL.Pos_product")
        
        # Fetch all rows
        rows = cursor.fetchall()

        result_dict = {'data':[]}  # Dict to store the final result
        print(result_dict)

        for row in rows:    
            # Extract values from the row
            Worker_Code, Line_no, Worker_name, Qty1 = row

            # Create a dictionary for the current row
            current_row_dict = {
                "Worker_Code": Worker_Code,
                "Line_no": Line_no,
                "Worker_name": Worker_name,
                "Qty1": Qty1,
            }

            # Add the current row dictionary to the result dictionary
            result_dict['data'].append(current_row_dict)
        print(result_dict)

        return jsonify(result_dict), HTTP_201_CREATED
    except Exception as e:
        Systemp_log(str(e), "Get_Quantity_Op").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
