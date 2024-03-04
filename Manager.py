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

Manager = Blueprint("Manager", __name__, url_prefix="/api/v1/Manager")

# Nếu hàng từ CNC qua: Thì mình chỉ việc sửa nếu sửa đc rồi đưa lại bên gia công tiếp tục gia công
@Manager.post('/Insert_Manager_History_Data')
@swag_from('./docs/Manager/Insert_Manager_History_Data.yaml')
def Insert_Manager_History_Data():
    try:
        Manager_Code = request.json['Manager_Code'] # Mã Quản Lý

        print("INSERT INTO [BonusCalculation].[dbo].[Manager_History](Manager_Code, TimeIn) VALUES ('"+ Manager_Code +"', GETDATE())")
        cursor.execute("INSERT INTO [BonusCalculation].[dbo].[Manager_History](Manager_Code, TimeIn) VALUES ('"+ Manager_Code +"', GETDATE())")
        conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Insert_Manager_History_Data").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify('OK'), HTTP_201_CREATED

@Manager.post('/Update_TimeOut_Manager_History')
@swag_from('./docs/Manager/Update_TimeOut_Manager_History.yaml')
def Update_TimeOut_Manager_History():
    try:
        Manager_Code = request.json['Manager_Code'] # Mã Quản Lý

        # Thưc thi câu lệnh
        print("UPDATE [BonusCalculation].[dbo].[Manager_History] SET TimeOut = GETDATE() WHERE Manager_Code = '" + Manager_Code + "' AND TimeOut IS NULL")
        cursor.execute("UPDATE [BonusCalculation].[dbo].[Manager_History] SET TimeOut = GETDATE() WHERE Manager_Code = '" + Manager_Code + "' AND TimeOut IS NULL")

        # Cập nhật sự thay đổi của table
        cursor.commit()
    except Exception as e:
        Systemp_log(str(e), "Update_TimeOut_Manager_History").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify('OK'), HTTP_201_CREATED

@Manager.post('/Save_Data_To_NG_Products_History')
@swag_from('./docs/Manager/Save_Data_To_NG_Products_History.yaml')
def Save_Data_To_NG_Products_History():
    try:
        Manager_Code = request.json['Manager_Code'] # Mã hàng hóa
        Worker_Code = request.json['Worker_Code'] # Mã hàng hóa
        Worker_Name = request.json['Worker_Name'] # Mã hàng hóa
        Product_Code = request.json['Product_Code'] # Mã hàng hóa
        Error_Code = request.json['Error_Code'] # Mã lỗi của con hàng
        Error_Detail = request.json['Error_Detail'] # Mã lỗi của con hàng
        Error_Position = request.json['Error_Position']
        Line_No = request.json['Line_No']
        Num_Subtraction = request.json['Num_Subtraction']
        CNCOrQC = request.json['CNCOrQC']
        Time_Error = request.json['Time_Error']

        # Thưc thi câu lệnh
        print("INSERT INTO [BonusCalculation].[dbo].[NG_Products_History](Manager_Code, Worker_Code, Worker_Name, Product_Code, Error_Code, Error_Detail, Error_Position, Line_No, Num_Subtraction, Time_Error, CNCOrQC, Time_Save) VALUES ('"+ Manager_Code +"', '"+ Worker_Code +"', N'"+ Worker_Name +"', '"+ Product_Code +"', '"+ Error_Code +"', N'"+ Error_Detail +"', N'"+ Error_Position +"', '"+ Line_No +"', '"+ Num_Subtraction +"', '"+ Time_Error +"', '"+ CNCOrQC +"', GETDATE())")
        if Time_Error != "NULL":
            cursor.execute("INSERT INTO [BonusCalculation].[dbo].[NG_Products_History](Manager_Code, Worker_Code, Worker_Name, Product_Code, Error_Code, Error_Detail, Error_Position, Line_No, Num_Subtraction, Time_Error, CNCOrQC, Time_Save) VALUES ('"+ Manager_Code +"', '"+ Worker_Code +"', N'"+ Worker_Name +"', '"+ Product_Code +"', '"+ Error_Code +"', N'"+ Error_Detail +"', N'"+ Error_Position +"', '"+ Line_No +"', '"+ Num_Subtraction +"', '"+ Time_Error +"', '"+ CNCOrQC +"', GETDATE())")
        else:
            cursor.execute("INSERT INTO [BonusCalculation].[dbo].[NG_Products_History](Manager_Code, Worker_Code, Worker_Name, Product_Code, Error_Code, Error_Detail, Error_Position, Line_No, Num_Subtraction, Time_Error, CNCOrQC, Time_Save) VALUES ('"+ Manager_Code +"', '"+ Worker_Code +"', N'"+ Worker_Name +"', '"+ Product_Code +"', '"+ Error_Code +"', N'"+ Error_Detail +"', N'"+ Error_Position +"', '"+ Line_No +"', '"+ Num_Subtraction +"', NULL, '"+ CNCOrQC +"', GETDATE())")
        
        # Cập nhật sự thay đổi của table
        cursor.commit()
    except Exception as e:
        Systemp_log(str(e), "Save_Data_To_Error_Products_History").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify('OK'), HTTP_201_CREATED

@Manager.post('/Save_Data_To_NG_Products_History_Repair')
@swag_from('./docs/Manager/Save_Data_To_NG_Products_History_Repair.yaml')
def Save_Data_To_NG_Products_History_Repair():
    try:
        Manager_Code = request.json['Manager_Code'] # Mã hàng hóa
        Worker_Code = request.json['Worker_Code'] # Mã hàng hóa
        Worker_Name = request.json['Worker_Name'] # Mã hàng hóa
        Product_Code = request.json['Product_Code'] # Mã hàng hóa
        Error_Code = request.json['Error_Code'] # Mã lỗi của con hàng
        Error_Detail = request.json['Error_Detail'] # Mã lỗi của con hàng
        Error_Position = request.json['Error_Position']
        Line_No = request.json['Line_No']
        Num_Subtraction = request.json['Num_Subtraction']
        CNCOrQC = request.json['CNCOrQC']
        Time_Error = request.json['Time_Error']
        Product_Type = request.json['Product_Type']
        Error_Location = request.json['Error_Location']
        Date_Shift = request.json["Date_Shift"]

        # Thưc thi câu lệnh
        if Time_Error != "NULL" and len(Date_Shift) != 0:
            cursor.execute("INSERT INTO [BonusCalculation].[dbo].[NG_Products_History](Manager_Code, Worker_Code, Worker_Name, Product_Code, Error_Code, Error_Detail, Error_Position, Line_No, Num_Subtraction, Time_Error, CNCOrQC, Product_Type, Error_Location, Date_Shift, Time_Save) VALUES ('"+ Manager_Code +"', '"+ Worker_Code +"', N'"+ Worker_Name +"', '"+ Product_Code +"', '"+ Error_Code +"', N'"+ Error_Detail +"', N'"+ Error_Position +"', '"+ Line_No +"', '"+ Num_Subtraction +"', '"+ Time_Error +"', '"+ CNCOrQC +"', '"+ Product_Type +"', '"+ Error_Location +"', '"+ Date_Shift +"', GETDATE())")
        elif Time_Error == "NULL" and len(Date_Shift) != 0:
            cursor.execute("INSERT INTO [BonusCalculation].[dbo].[NG_Products_History](Manager_Code, Worker_Code, Worker_Name, Product_Code, Error_Code, Error_Detail, Error_Position, Line_No, Num_Subtraction, Time_Error, CNCOrQC, Product_Type, Error_Location, Date_Shift, Time_Save) VALUES ('"+ Manager_Code +"', '"+ Worker_Code +"', N'"+ Worker_Name +"', '"+ Product_Code +"', '"+ Error_Code +"', N'"+ Error_Detail +"', N'"+ Error_Position +"', '"+ Line_No +"', '"+ Num_Subtraction +"', NULL, '"+ CNCOrQC +"', '"+ Product_Type +"', '"+ Error_Location +"', '"+ Date_Shift +"', GETDATE())")
        elif Time_Error != "NULL" and len(Date_Shift) == 0:
            print("INSERT INTO [BonusCalculation].[dbo].[NG_Products_History](Manager_Code, Worker_Code, Worker_Name, Product_Code, Error_Code, Error_Detail, Error_Position, Line_No, Num_Subtraction, Time_Error, CNCOrQC, Product_Type, Error_Location, Date_Shift, Time_Save) VALUES ('"+ Manager_Code +"', '"+ Worker_Code +"', N'"+ Worker_Name +"', '"+ Product_Code +"', '"+ Error_Code +"', N'"+ Error_Detail +"', N'"+ Error_Position +"', '"+ Line_No +"', '"+ Num_Subtraction +"', '" + Time_Error + "', '"+ CNCOrQC +"', '"+ Product_Type +"', '"+ Error_Location +"', NULL, GETDATE())")
            cursor.execute("INSERT INTO [BonusCalculation].[dbo].[NG_Products_History](Manager_Code, Worker_Code, Worker_Name, Product_Code, Error_Code, Error_Detail, Error_Position, Line_No, Num_Subtraction, Time_Error, CNCOrQC, Product_Type, Error_Location, Date_Shift, Time_Save) VALUES ('"+ Manager_Code +"', '"+ Worker_Code +"', N'"+ Worker_Name +"', '"+ Product_Code +"', '"+ Error_Code +"', N'"+ Error_Detail +"', N'"+ Error_Position +"', '"+ Line_No +"', '"+ Num_Subtraction +"', '" + Time_Error + "', '"+ CNCOrQC +"', '"+ Product_Type +"', '"+ Error_Location +"', NULL, GETDATE())")
        elif Time_Error == "NULL" and len(Date_Shift) == 0:
            cursor.execute("INSERT INTO [BonusCalculation].[dbo].[NG_Products_History](Manager_Code, Worker_Code, Worker_Name, Product_Code, Error_Code, Error_Detail, Error_Position, Line_No, Num_Subtraction, Time_Error, CNCOrQC, Product_Type, Error_Location, Date_Shift, Time_Save) VALUES ('"+ Manager_Code +"', '"+ Worker_Code +"', N'"+ Worker_Name +"', '"+ Product_Code +"', '"+ Error_Code +"', N'"+ Error_Detail +"', N'"+ Error_Position +"', '"+ Line_No +"', '"+ Num_Subtraction +"', NULL, '"+ CNCOrQC +"', '"+ Product_Type +"', '"+ Error_Location +"', NULL, GETDATE())")
        
        # Cập nhật sự thay đổi của table
        cursor.commit()

    except Exception as e:
        Systemp_log(str(e), "Save_Data_To_NG_Products_History_Repair").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify('OK'), HTTP_201_CREATED

@Manager.post("/Get_Distinct_NG_Productivity_Today_Realtime_By_Worker_Code")
@swag_from("./docs/Manager/Get_Distinct_NG_Productivity_Today_Realtime_By_Worker_Code.yaml")
def Get_Distinct_NG_Productivity_Today_Realtime_By_Worker_Code():
    try:
        today = datetime.datetime.now()
        ytday = today - datetime.timedelta(days=1)
        if today.hour < 8 or today.hour >= 20:
            if today.hour < 8:
                cursor.execute("select count(distinct(DMC)) as count from [QC].[dbo].[CMMdata] where TimeSave > '" + today.strftime("%Y-%m-%d 08:00:00'"))
                print("select count(distinct(Product_Code)) as TotalDistinctProductCode from [BonusCalculation].[dbo].[NG_Products_History] where Time_Save > '" + ytday.strftime("%Y-%m-%d 20:00:00'"))
                cursor.execute("select count(distinct(Product_Code)) as TotalDistinctProductCode from [BonusCalculation].[dbo].[NG_Products_History] where Time_Save > '" + ytday.strftime("%Y-%m-%d 20:00:00'"))
                result = cursor.fetchone()
                count = result[0]
            elif today.hour >= 20:
                print("select count(distinct(Product_Code)) as TotalDistinctProductCode from [BonusCalculation].[dbo].[NG_Products_History] where Time_Save > '" + today.strftime("%Y-%m-%d 20:00:00'"))
                cursor.execute("select count(distinct(Product_Code)) as TotalDistinctProductCode from [BonusCalculation].[dbo].[NG_Products_History] where Time_Save > '" + today.strftime("%Y-%m-%d 20:00:00'"))
                result = cursor.fetchone()
                count = result[0]
        else:
            print("select count(distinct(Product_Code)) as TotalDistinctProductCode from [BonusCalculation].[dbo].[NG_Products_History] where Time_Save > '" + today.strftime("%Y-%m-%d 08:00:00'"))
            cursor.execute("select count(distinct(Product_Code)) as TotalDistinctProductCode from [BonusCalculation].[dbo].[NG_Products_History] where Time_Save > '" + today.strftime("%Y-%m-%d 08:00:00'"))
            result = cursor.fetchone()
            count = result[0]

        # Cập nhật sự thay đổi của table
        cursor.commit()
    except Exception as e:
        Systemp_log(str(e), "Get_Distinct_NG_Productivity_Today_Realtime_By_Worker_Code").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify({'count': count}), HTTP_201_CREATED

@Manager.post('/Check_Username_And_Password_Of_WorkerManager')
@swag_from('./docs/Manager/Check_Username_And_Password_Of_WorkerManager.yaml')
def Check_Username_And_Password_Of_WorkerManager():
    try:
        Worker_Code = request.json['Worker_Code']
        Password = request.json['Password']

        # Thưc thi câu lệnh
        print("select COUNT(*) AS CHECK_USERNAME_PASSWORD from [BonusCalculation].[dbo].[Worker_Manager] where Worker_Code  = '" + Worker_Code + "' and Password  = '" + Password + "'")
        cursor.execute("select COUNT(*) AS CHECK_USERNAME_PASSWORD from [BonusCalculation].[dbo].[Worker_Manager] where Worker_Code  = '" + Worker_Code + "' and Password  = '" + Password + "'")
        result = cursor.fetchone()
        count = result[0]

        # Cập nhật sự thay đổi của table
        cursor.commit()
    except Exception as e:
        Systemp_log(str(e), "Check_Username_And_Password_Of_WorkerManager").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify({'count': count}), HTTP_201_CREATED

@Manager.post('/Get_CNC_Product_Detail')
@swag_from('./docs/Manager/Get_CNC_Product_Detail.yaml')
def Get_CNC_Product_Detail():
    try:
        Product_Code = request.json['Product_Code']

        cursor.execute("select Machine_History.Worker_Code, Worker_Manager.Worker_Name, [Machine_CNC].OP2, [Machine_CNC].[Line_no],[DMC_product], [TimeoutCNC2], Machine_History.Date as Date_Shift from [QC].[dbo].[CNC] left join [BonusCalculation].[dbo].[Machine_CNC] on [CNC].Machineno = [Machine_CNC].Machineno and [CNC].Pos_product = [Machine_CNC].Pos_product left join [BonusCalculation].[dbo].Machine_History on Machine_CNC.OP2 = Machine_History.Machine join [BonusCalculation].[dbo].[Worker_Manager] on [Machine_History].Worker_Code = [Worker_Manager].Worker_Code where [DMC_product] = '"+Product_Code+"' and [CNC].TimeoutCNC2 <= ISNULL(Machine_History.TimeOut, GETDATE()) and [CNC].TimeoutCNC2 >= Machine_History.TimeIn")
        
        # Fetch all rows
        rows = cursor.fetchall()

        result_dict = {}  # Dict to store the final result

        for row in rows:
            # Extract values from the row
            Worker_Code, Worker_Name, OP2, Line_no, DMC_product, TimeoutCNC2, Date_Shift = row
            formatted_timeout = TimeoutCNC2.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            date_shift = datetime.datetime.strptime(Date_Shift, '%Y-%m-%d')

            # Create a dictionary for the current row
            current_row_dict = {
                "Worker_Code": Worker_Code,
                "Worker_Name": Worker_Name,
                "OP2": OP2,
                "Line_no": Line_no,
                "DMC_product": DMC_product,
                "TimeoutCNC2": formatted_timeout,
                "Date_Shift": date_shift
            }

            # Add the current row dictionary to the result dictionary
            result_dict[DMC_product] = current_row_dict

        return jsonify(result_dict), HTTP_201_CREATED

    except Exception as e:
        Systemp_log(str(e), "Get_CNC_Product_Detail").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})

@Manager.post('/Get_OP3_Product_Detail')
@swag_from('./docs/Manager/Get_OP3_Product_Detail.yaml')
def Get_OP3_Product_Detail():
    try:
        Product_Code = request.json['Product_Code']

        cursor.execute("select c.Worker_Code, d.Worker_Name, b.OP2, b.Line_no, a.DMC_product, a.Time_out, e.TimeoutCNC2 from [GC].[dbo].[OP3_data] a left join [BonusCalculation].[dbo].[Machine_CNC] b on a.Line_no = b.Machineno join [BonusCalculation].[dbo].[Machine_History] c on b.OP2 = c.Machine join [BonusCalculation].[dbo].[Worker_Manager] d on c.Worker_Code = d.Worker_Code join [QC].[dbo].[CNC] e on e.Machineno = b.Machineno and e.Pos_product = b.Pos_product where a.DMC_product = '"+ Product_Code +"' and a.Time_out <= c.TimeOut and a.Time_out >= c.TimeIn")
        
        # Fetch all rows
        rows = cursor.fetchall()

        result_dict = {}  # Dict to store the final result

        for row in rows:
            # Extract values from the row
            Worker_Code, Worker_Name, OP2, Line_no, DMC_product, Time_out, TimeoutCNC2 = row
            formatted_timeout = Time_out.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            formatted_timeout_cnc2 = TimeoutCNC2.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

            # Create a dictionary for the current row
            current_row_dict = {
                "Worker_Code": Worker_Code,
                "Worker_Name": Worker_Name,
                "OP2": OP2,
                "Line_no": Line_no,
                "DMC_product": DMC_product,
                "Time_out": formatted_timeout,
                "TimeoutCNC2": formatted_timeout_cnc2
            }

            # Add the current row dictionary to the result dictionary
            result_dict[DMC_product] = current_row_dict

        return jsonify(result_dict), HTTP_201_CREATED

    except Exception as e:
        Systemp_log(str(e), "Get_OP3_Product_Detail").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})

@Manager.post('/Get_Bavia_Product_Detail')
@swag_from('./docs/Manager/Get_Bavia_Product_Detail.yaml')
def Get_Bavia_Product_Detail():
    try:
        Product_Code = request.json['Product_Code']

        cursor.execute("select c.Worker_Code, d.Worker_Name, b.OP2, b.Line_no, a.Product_Code, a.TimeSave, e.TimeoutCNC2 from [BonusCalculation].[dbo].[Bavia_Products] a left join [BonusCalculation].[dbo].[Machine_CNC] b on a.Bavia_Code = b.Machineno  join [BonusCalculation].[dbo].[Machine_History] c on b.OP2 = c.Machine join [BonusCalculation].[dbo].[Worker_Manager] d on c.Worker_Code = d.Worker_Code join [QC].[dbo].[CNC] e on e.Machineno = b.Machineno and e.Pos_product = b.Pos_product where a.Product_Code = '"+Product_Code+"' and a.TimeSave <= c.TimeOut and a.TimeSave >= c.TimeIn")
        
        # Fetch all rows
        rows = cursor.fetchall()

        result_dict = {}  # Dict to store the final result

        for row in rows:
            # Extract values from the row
            Worker_Code, Worker_Name, OP2, Line_no, DMC_product, TimeSave, TimeoutCNC2 = row
            formatted_timesave = TimeSave.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            formatted_timeout_cnc2 = TimeoutCNC2.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

            # Create a dictionary for the current row
            current_row_dict = {
                "Worker_Code": Worker_Code,
                "Worker_Name": Worker_Name,
                "OP2": OP2,
                "Line_no": Line_no,
                "DMC_product": DMC_product,
                "TimeSave": formatted_timesave,
                "TimeoutCNC2": formatted_timeout_cnc2
            }

            # Add the current row dictionary to the result dictionary
            result_dict[DMC_product] = current_row_dict

        return jsonify(result_dict), HTTP_201_CREATED

    except Exception as e:
        Systemp_log(str(e), "Get_Bavia_Product_Detail").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
