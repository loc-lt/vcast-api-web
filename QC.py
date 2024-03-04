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

QC = Blueprint("QC", __name__, url_prefix="/api/v1/QC")

# Thêm lịch sử sử dụng máy mỗi lần quét máy (Cũng áp dụng cho cả Biavia lẫn tẩy rửa) => KHÔNG CẦN LÀM LẠI

# Thêm từng con hàng vào bảng QC_Products_History (Ở mỗi bước của QC, khi quét thì nó sẽ hiện ra 1 cái giao
# diện, sẽ hiện ra 2 giá trị ErrorCheckingStep, Product_Code và để Null 3 giá trị kia cho bên QC điền), sau 
# khi nhập xong mới đưa -> Mình ko cần viết API để xuất ra 2 cái kia thì nó đã rõ nhờ vào MC bên QC và Mã hàng
# => SAU KHI NHẬP XONG THÌ SẼ LÀM SỬ DỤNG CÁI API NÀY
# NOTE: thay vì chuyển ở các công đoạn khác thì ở đây có ErrorCheckingStep

@QC.post('/Insert_QC_Products_History')
@swag_from('./docs/QC/Insert_QC_Products_History.yaml')
def Insert_QC_Products_History():
    try:
        ErrorCheckingStep = request.json['ErrorCheckingStep'] # Bước check lỗi trong QC
        Product_Code = request.json['Product_Code'] # Mã hàng hóa
        ErrorCode = request.json['ErrorCode'] # Mã lỗi của con hàng
        OK_NG = request.json['OK_NG'] # Con hàng có lỗi hay ko
        ErrorDetail = request.json['ErrorDetail'] # Chi tiết lỗi

        # ErrorCode: Mã lỗi của con hàng vừa vào mỗi bước của QC, lúc mới quét hàng ở mỗi bước ở QC thì
        # là Null, sau đó nếu đi qua các bước của QC nếu phát hiện lỗi ở bước nào thì cập nhật
        # OK_NG: Con hàng đó có OK hay ko, OK thì là "1", NG thì là "0", một con hàng được xem là
        # sửa thành công nếu OK-NG ở tất cả các bước là "1", lúc mới vô cx là Null, QC sẽ cập nhật
        # ErrorDetail: Lúc đầu cũng là Null

        print("INSERT INTO [BonusCalculation].[dbo].[QC_Products_History](ErrorCheckingStep, Product_Code, ErrorCode, OK_NG, ErrorDetail, TimeSave)"
            " VALUES ('" + ErrorCheckingStep + "','" + Product_Code + "', '" + ErrorCode + "', '" + OK_NG + "','" + ErrorDetail + "', '" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "')")
        cursor.execute("INSERT INTO [BonusCalculation].[dbo].[QC_Products_History](ErrorCheckingStep, Product_Code, ErrorCode, OK_NG, ErrorDetail, TimeSave)"
            " VALUES ('" + ErrorCheckingStep + "','" + Product_Code + "', '" + ErrorCode + "', '" + OK_NG + "','" + ErrorDetail + "', '" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "')")
        conn.commit()

    except Exception as e:
        Systemp_log(str(e), "Insert_QC_Products_History").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify('OK'), HTTP_201_CREATED

# Khi từng bộ phận của QC quét mã Barcode, phải check lại thử mã lỗi này của
# con hàng này đã từng bị chưa, chưa bị thì thêm mới 1 dòng dữ liệu còn có rồi
# thì tạm thời đưa thẳng vào kho phế liệu
@QC.post('/Check_Errorcode_Of_Product')
@swag_from('./docs/QC/Check_Errorcode_Of_Product.yaml')
def Check_Errorcode_Of_Product():
    try:
        Product_Code = request.json['Product_Code'] # Mã hàng hóa
        ErrorCode = request.json['ErrorCode'] # Mã lỗi của con hàng

        # Thưc thi câu lệnh
        print("SELECT COUNT(*) AS ERROR_APPEAR FROM [BonusCalculation].[dbo].[QC_Products_History] WHERE Product_Code = '" + Product_Code + "' and ErrorCode = '" + ErrorCode + "' and DATEDIFF(MINUTE, (SELECT TOP(1) TimeSave FROM [BonusCalculation].[dbo].[QC_Products_History] WHERE Product_Code = '" + Product_Code + "' and ErrorCode = '" + ErrorCode + "' ORDER BY TimeSave DESC), GETDATE()) > 0 AND DATEDIFF(MINUTE, (SELECT TOP(1) TimeSave FROM [BonusCalculation].[dbo].[QC_Products_History] WHERE Product_Code = '" + Product_Code + "' and ErrorCode = '" + ErrorCode + "' ORDER BY TimeSave DESC), GETDATE()) < 720")
        cursor.execute("SELECT COUNT(*) AS ERROR_APPEAR FROM [BonusCalculation].[dbo].[QC_Products_History] WHERE Product_Code = '" + Product_Code + "' and ErrorCode = '" + ErrorCode + "' and DATEDIFF(MINUTE, (SELECT TOP(1) TimeSave FROM [BonusCalculation].[dbo].[QC_Products_History] WHERE Product_Code = '" + Product_Code + "' and ErrorCode = '" + ErrorCode + "' ORDER BY TimeSave DESC), GETDATE()) > 0 AND DATEDIFF(MINUTE, (SELECT TOP(1) TimeSave FROM [BonusCalculation].[dbo].[QC_Products_History] WHERE Product_Code = '" + Product_Code + "' and ErrorCode = '" + ErrorCode + "' ORDER BY TimeSave DESC), GETDATE()) < 720")
        result = cursor.fetchone()
        count = result[0]

        # Cập nhật sự thay đổi của table
        cursor.commit()
    except Exception as e:
        Systemp_log(str(e), "Check_Errorcode_Of_Product").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify({'count': count}), HTTP_201_CREATED

@QC.post('/Update_OK_NG_From_QC_Products_History')
@swag_from('./docs/QC/Update_OK_NG_From_QC_Products_History.yaml')
def Update_OK_NG_From_QC_Products_History():
    try:
        Product_Code = request.json['Product_Code'] # Mã hàng hóa
        ErrorCode = request.json['ErrorCode'] # Mã lỗi của con hàng
        OK_NG = request.json['OK_NG']

        # Thưc thi câu lệnh
        print("UPDATE [BonusCalculation].[dbo].[QC_Products_History] SET OK_NG = '" + OK_NG + "' WHERE Product_Code = '" + Product_Code + "' AND ErrorCode = '" + ErrorCode + "' AND DATEDIFF(MINUTE, TimeSave, GETDATE()) > 0 AND DATEDIFF(MINUTE, TimeSave, GETDATE()) < 720 ")
        cursor.execute("UPDATE [BonusCalculation].[dbo].[QC_Products_History] SET OK_NG = '" + OK_NG + "' WHERE Product_Code = '" + Product_Code + "' AND ErrorCode = '" + ErrorCode + "' AND DATEDIFF(MINUTE, TimeSave, GETDATE()) > 0 AND DATEDIFF(MINUTE, TimeSave, GETDATE()) < 720 ")

        # Cập nhật sự thay đổi của table
        cursor.commit()
    except Exception as e:
        Systemp_log(str(e), "Update_OK_NG_From_QC_Products_History").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify('OK'), HTTP_201_CREATED

@QC.post('/Insert_Data_Into_AirGauge036')
@swag_from('./docs/QC/Insert_Data_Into_AirGauge036.yaml')
def Insert_Data_Into_AirGauge036():
    try:
        Machine = request.json['Machine'] # Mã hàng hóa
        Product_Name = request.json['Product_Name'] # Mã lỗi của con hàng
        Time_ScanDMC = request.json['Time_ScanDMC']
        TimeFinish = request.json['TimeFinish']
        DMC = request.json['DMC']
        MachiningStation = request.json['MachiningStation']
        Operator = request.json['Operator']
        P6_Min = request.json['P6_Min']
        P6_Max = request.json['P6_Max']
        P10_1_Min = request.json['P10_1_Min']
        P10_1_Max = request.json['P10_1_Max']
        P10_2_Min = request.json['P10_2_Min']
        P10_2_Max = request.json['P10_2_Max']
        P13_Min = request.json['P13_Min']
        P13_Max = request.json['P13_Max']
        P18_1_Min = request.json['P18_1_Min']
        P18_1_Max = request.json['P18_1_Max']
        P18_2_Min = request.json['P18_2_Min']
        P18_2_Max = request.json['P18_2_Max']
        P53_Min = request.json['P53_Min']
        P53_Max = request.json['P53_Max']
        Result = request.json['Result']
        Pin_Ring = request.json['Pin_Ring']

        # Thưc thi câu lệnh
        print("Tao vào rồi")
        print("INSERT INTO [QC].[dbo].[AirGauge036] ([Machine], [Product_Name], [Time_ScanDMC], [TimeFinish], [DMC], [MachiningStation], [Operator], [P6_Min], [P6_Max], [P10_1_Min], [P10_1_Max], [P10_2_Min], [P10_2_Max], [P13_Min], [P13_Max], [P18_1_Min], [P18_1_Max], [P18_2_Min], [P18_2_Max], [P53_Min], [P53_Max], [Result], [Pin_Ring]) VALUES ( '" + Machine + "', '" + Product_Name + "', '" + Time_ScanDMC + "', '" + TimeFinish + "', '" + DMC + "', '" + MachiningStation + "' , '" +  Operator+ "', '" + P6_Min + "', '" + P6_Max + "', '" + P10_1_Min + "', '" + P10_1_Max + "', '" + P10_2_Min + "', '" + P10_2_Max + "', '" + P13_Min + "', '" + P13_Max + "', '" + P18_1_Min + "', '" + P18_1_Max + "', '" + P18_2_Min + "', '" + P18_2_Max + "', '" + P53_Min + "', '" + P53_Max + "', '" + Result + "', '" + Pin_Ring + "')")
        cursor.execute("INSERT INTO [QC].[dbo].[AirGauge036] ([Machine], [Product_Name], [Time_ScanDMC], [TimeFinish], [DMC], [MachiningStation], [Operator], [P6_Min], [P6_Max], [P10_1_Min], [P10_1_Max], [P10_2_Min], [P10_2_Max], [P13_Min], [P13_Max], [P18_1_Min], [P18_1_Max], [P18_2_Min], [P18_2_Max], [P53_Min], [P53_Max], [Result], [Pin_Ring]) VALUES ( '" + Machine + "', '" + Product_Name + "', '" + Time_ScanDMC + "', '" + TimeFinish + "', '" + DMC + "', '" + MachiningStation + "' , '" +  Operator+ "', '" + P6_Min + "', '" + P6_Max + "', '" + P10_1_Min + "', '" + P10_1_Max + "', '" + P10_2_Min + "', '" + P10_2_Max + "', '" + P13_Min + "', '" + P13_Max + "', '" + P18_1_Min + "', '" + P18_1_Max + "', '" + P18_2_Min + "', '" + P18_2_Max + "', '" + P53_Min + "', '" + P53_Max + "', '" + Result + "', '" + Pin_Ring + "')")

        # Cập nhật sự thay đổi của table
        cursor.commit()
    except Exception as e:
        Systemp_log(str(e), "Insert_Data_Into_AirGauge036").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify('OK'), HTTP_201_CREATED

@QC.post('/Insert_Data_Into_AirGauge036_Repair')
@swag_from('./docs/QC/Insert_Data_Into_AirGauge036_Repair.yaml')
def Insert_Data_Into_AirGauge036_Repair():
    try:
        Machine = request.json['Machine'] # Mã hàng hóa
        Product_Name = request.json['Product_Name'] # Mã lỗi của con hàng
        Time_ScanDMC = request.json['Time_ScanDMC']
        TimeFinish = request.json['TimeFinish']
        Furnace = request.json['Furnace']
        DMC = request.json['DMC']
        MachiningStation = request.json['MachiningStation']
        Operator = request.json['Operator']
        P6_Min = request.json['P6_Min']
        P6_Max = request.json['P6_Max']
        P10_1_Min = request.json['P10_1_Min']
        P10_1_Max = request.json['P10_1_Max']
        P10_2_Min = request.json['P10_2_Min']
        P10_2_Max = request.json['P10_2_Max']
        P13_Min = request.json['P13_Min']
        P13_Max = request.json['P13_Max']
        P18_1_Min = request.json['P18_1_Min']
        P18_1_Max = request.json['P18_1_Max']
        P18_2_Min = request.json['P18_2_Min']
        P18_2_Max = request.json['P18_2_Max']
        P53_Min = request.json['P53_Min']
        P53_Max = request.json['P53_Max']
        Result = request.json['Result']
        Pin_Ring = request.json['Pin_Ring']
        Note = request.json['Note']

        # Thưc thi câu lệnh
        print("INSERT INTO [QC].[dbo].[AirGauge036] ([Machine], [Product_Name], [Time_ScanDMC], [TimeFinish], [Furnace], [DMC], [MachiningStation], [Operator], [P6_Min], [P6_Max], [P10_1_Min], [P10_1_Max], [P10_2_Min], [P10_2_Max], [P13_Min], [P13_Max], [P18_1_Min], [P18_1_Max], [P18_2_Min], [P18_2_Max], [P53_Min], [P53_Max], [Result], [Pin_Ring], [Note]) VALUES ( '" + Machine + "', '" + Product_Name + "', '" + Time_ScanDMC + "', '" + TimeFinish + "', '" + Furnace + "', '" + DMC + "', '" + MachiningStation + "' , '" +  Operator+ "', '" + P6_Min + "', '" + P6_Max + "', '" + P10_1_Min + "', '" + P10_1_Max + "', '" + P10_2_Min + "', '" + P10_2_Max + "', '" + P13_Min + "', '" + P13_Max + "', '" + P18_1_Min + "', '" + P18_1_Max + "', '" + P18_2_Min + "', '" + P18_2_Max + "', '" + P53_Min + "', '" + P53_Max + "', '" + Result + "', '" + Pin_Ring + "', '" + Note + "')")
        cursor.execute("INSERT INTO [QC].[dbo].[AirGauge036] ([Machine], [Product_Name], [Time_ScanDMC], [TimeFinish], [Furnace], [DMC], [MachiningStation], [Operator], [P6_Min], [P6_Max], [P10_1_Min], [P10_1_Max], [P10_2_Min], [P10_2_Max], [P13_Min], [P13_Max], [P18_1_Min], [P18_1_Max], [P18_2_Min], [P18_2_Max], [P53_Min], [P53_Max], [Result], [Pin_Ring], [Note]) VALUES ( '" + Machine + "', '" + Product_Name + "', '" + Time_ScanDMC + "', '" + TimeFinish + "', '" + Furnace + "', '" + DMC + "', '" + MachiningStation + "' , '" +  Operator+ "', '" + P6_Min + "', '" + P6_Max + "', '" + P10_1_Min + "', '" + P10_1_Max + "', '" + P10_2_Min + "', '" + P10_2_Max + "', '" + P13_Min + "', '" + P13_Max + "', '" + P18_1_Min + "', '" + P18_1_Max + "', '" + P18_2_Min + "', '" + P18_2_Max + "', '" + P53_Min + "', '" + P53_Max + "', '" + Result + "', '" + Pin_Ring + "', '" + Note + "')")

        # Cập nhật sự thay đổi của table
        cursor.commit()
    except Exception as e:
        Systemp_log(str(e), "Insert_Data_Into_AirGauge036_Repair").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify('OK'), HTTP_201_CREATED

@QC.post('/Insert_Data_Into_AirGauge036_Classification')
@swag_from('./docs/QC/Insert_Data_Into_AirGauge036_Classification.yaml')
def Insert_Data_Into_AirGauge036_Classification():
    try:
        TimeDMC = request.json['TimeDMC'] # Mã hàng hóa
        CodeFurnace = request.json['CodeFurnace'] # Mã lỗi của con hàng
        DMC = request.json['DMC']
        PalletCode = request.json['PalletCode']
        DrawID = request.json['DrawID']
        DrawVersion = request.json['DrawVersion']
        Num = request.json['Num']

        # Thưc thi câu lệnh
        print("insert into [QC].[dbo].[AirGauge036_Classification] (TimeDMC, CodeFurnace, DMC, PalletCode, DrawID, DrawVersion, Num) values ('"+ TimeDMC +"', '"+ CodeFurnace +"', '"+ DMC +"', '"+ PalletCode +"', '"+ DrawID +"', '"+ DrawVersion +"', '"+ Num +"' )")
        cursor.execute("insert into [QC].[dbo].[AirGauge036_Classification] (TimeDMC, CodeFurnace, DMC, PalletCode, DrawID, DrawVersion, Num) values ('"+ TimeDMC +"', '"+ CodeFurnace +"', '"+ DMC +"', '"+ PalletCode +"', '"+ DrawID +"', '"+ DrawVersion +"', '"+ Num +"')")

        # Cập nhật sự thay đổi của table
        cursor.commit()
    except Exception as e:
        Systemp_log(str(e), "Insert_Data_Into_AirGauge036_Classification").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify('OK'), HTTP_201_CREATED

@QC.post('/Insert_Data_Into_AirGauge036_Classification_Repair')
@swag_from('./docs/QC/Insert_Data_Into_AirGauge036_Classification_Repair.yaml')
def Insert_Data_Into_AirGauge036_Classification_Repair():
    try:
        TimeDMC = request.json['TimeDMC'] # Mã hàng hóa
        DMC = request.json['DMC']
        PalletCode = request.json['PalletCode']
        DrawID = request.json['DrawID']
        DrawVersion = request.json['DrawVersion']
        Num = request.json['Num']

        # Thưc thi câu lệnh
        print("insert into [QC].[dbo].[AirGauge036_Classification] (TimeDMC, DMC, PalletCode, DrawID, DrawVersion, Num) values ('"+ TimeDMC +"',, '"+ DMC +"', '"+ PalletCode +"', '"+ DrawID +"', '"+ DrawVersion +"', '"+ Num +"' )")
        cursor.execute("insert into [QC].[dbo].[AirGauge036_Classification] (TimeDMC, DMC, PalletCode, DrawID, DrawVersion, Num) values ('"+ TimeDMC +"', '"+ DMC +"', '"+ PalletCode +"', '"+ DrawID +"', '"+ DrawVersion +"', '"+ Num +"')")

        # Cập nhật sự thay đổi của table
        cursor.commit()
    except Exception as e:
        Systemp_log(str(e), "Insert_Data_Into_AirGauge036_Classification_Repair").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify('OK'), HTTP_201_CREATED

@QC.post('/Check_DMC_In_AirGauge036')
@swag_from('./docs/QC/Check_DMC_In_AirGauge036.yaml')
def Check_DMC_In_AirGauge036():
    try:
        DMC = request.json['DMC']

        # Thưc thi câu lệnh
        print("select COUNT(DMC) AS NUM_DMC from [QC].[dbo].[AirGauge036] where DMC  = '" + DMC + "'")
        cursor.execute("select COUNT(DMC) AS NUM_DMC from [QC].[dbo].[AirGauge036] where DMC  = '" + DMC + "'")
        result = cursor.fetchone()
        count = result[0]

        # Cập nhật sự thay đổi của table
        cursor.commit()
    except Exception as e:
        Systemp_log(str(e), "Check_DMC_In_AirGauge036").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify({'count': count}), HTTP_201_CREATED

@QC.post('/Check_DMC_In_AirGauge036_Classification')
@swag_from('./docs/QC/Check_DMC_In_AirGauge036_Classification.yaml')
def Check_DMC_In_AirGauge036_Classification():
    try:
        DMC = request.json['DMC']

        # Thưc thi câu lệnh
        print("select COUNT(DMC) AS NUM_DMC from [QC].[dbo].[AirGauge036_Classification] where DMC  = '" + DMC + "'")
        cursor.execute("select COUNT(DMC) AS NUM_DMC from AirGauge036_Classification where DMC  = '" + DMC + "'")
        result = cursor.fetchone()
        count = result[0]

        # Cập nhật sự thay đổi của table
        cursor.commit()
    except Exception as e:
        Systemp_log(str(e), "Check_DMC_In_AirGauge036_Classification").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify({'count': count}), HTTP_201_CREATED

@QC.post('/Insert_Data_Into_AirTight036')
@swag_from('./docs/QC/Insert_Data_Into_AirTight036.yaml')
def Insert_Data_Into_AirTight036():
    try:
        TimeStart = request.json['TimeStart'] # Mã hàng hóa
        TimeFinish = request.json['TimeFinish'] # Mã lỗi của con hàng
        Machine = request.json['Machine']
        DMC = request.json['DMC']
        AirValue_1 = request.json['AirValue_1']
        Result_Station_1 = request.json['Result_Station_1']
        AirValue_2 = request.json['AirValue_2']
        Result_Station_2 = request.json['Result_Station_2']
        Total_Quality = request.json['Total_Quality']
        Note = request.json['Note']
        Note1 = request.json['Note1']
        Note2 = request.json['Note2']
        Note3 = request.json['Note3']
        Note4 = request.json['Note4']
        Note5 = request.json['Note5']

        # Thưc thi câu lệnh
        print("insert into [QC].[dbo].[AirTight036] ([TimeStart],[TimeFinish],[Machine],[DMC],[AirValue_1],[Result_Station_1],[AirValue_2],[Result_Station_2],[Total_Quality],[Note],[Note1],[Note2],[Note3],[Note4],[Note5]) VALUES ( '" + TimeStart + "', '" + TimeFinish + "', '" + Machine + "', '" + DMC + "', '" + AirValue_1 + "', '" + Result_Station_1 + "' , '" +  AirValue_2 + "', '" + Result_Station_2 + "', '" + Total_Quality + "', '" + Note + "', '" + Note1 + "', '" + Note2 + "', '" + Note3 + "', '" + Note4 + "', '" + Note5 + "')")
        cursor.execute("insert into [QC].[dbo].[AirTight036] ([TimeStart],[TimeFinish],[Machine],[DMC],[AirValue_1],[Result_Station_1],[AirValue_2],[Result_Station_2],[Total_Quality],[Note],[Note1],[Note2],[Note3],[Note4],[Note5]) VALUES ( '" + TimeStart + "', '" + TimeFinish + "', '" + Machine + "', '" + DMC + "', '" + AirValue_1 + "', '" + Result_Station_1 + "' , '" +  AirValue_2 + "', '" + Result_Station_2 + "', '" + Total_Quality + "', '" + Note + "', '" + Note1 + "', '" + Note2 + "', '" + Note3 + "', '" + Note4 + "', '" + Note5 + "')")

        # Cập nhật sự thay đổi của table
        cursor.commit()
    except Exception as e:
        Systemp_log(str(e), "Insert_Data_Into_AirTight036").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify('OK'), HTTP_201_CREATED

