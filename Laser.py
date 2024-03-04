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
cursor.execute('Select Time_reset From Serial_laser')
dt =cursor.fetchall()[0][0]
Laser = Blueprint("Laser", __name__, url_prefix="/api/v1/Laser")
@Laser.get("/update_serial/<string:NameProduct>")
@swag_from("./docs/Laser/serial.yaml")
def update_serial(NameProduct):
     try:
     # thuc=pd.read_sql("Select*From Serial_laser",conn)
         cursor.execute("Select Serial From Serial_laser where NameProduct ='"+NameProduct+"'")
         Data = cursor.fetchall()
         i=str(Data[0][0]+1)
         cursor.execute("UPDATE Serial_laser SET Serial = '"+i+"'where NameProduct ='"+NameProduct+"'")
         conn.commit()
         result=Dataget_Laser.dump(Data)
     except Exception as e:
        Systemp_log(str(e), "update_serial").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
     return jsonify({'data':result}), HTTP_200_OK

@Laser.get("/get_serial/<string:NameProduct>")
@swag_from("./docs/Laser/get_serial.yaml")
def get_serial(NameProduct):
    try:
         # thuc=pd.read_sql("Select*From Serial_laser",conn)
         cursor.execute("Select Serial From Serial_laser where NameProduct ='"+NameProduct+"'")
         Data = cursor.fetchall()
         result=Dataget_Laser.dump(Data)
    except Exception as e:
        Systemp_log(str(e), "get_serial").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify({'data':result}), HTTP_200_OK

@Laser.post('/set_serial')
@swag_from('./docs/Laser/set_serial.yaml')
def set_serial():
    try:
        Serial = request.json['Serial']
        NameProduct = request.json['NameProduct']
        cursor.execute("UPDATE Serial_laser SET Serial = '" + Serial + "'where NameProduct ='" + NameProduct + "'")
        conn.commit()
    except Exception as e:
        Systemp_log(str(e), "set_serial").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify('OK'),HTTP_201_CREATED

@Laser.get("/get_waxmold/<string:NameProduct>")
@swag_from("./docs/Laser/get_waxmold.yaml")
def get_waxmold(NameProduct):
    try:
         # thuc=pd.read_sql("Select*From Serial_laser",conn)
         cursor.execute("Select Waxmold From Serial_laser where NameProduct ='"+NameProduct+"'")
         Data = cursor.fetchall()
         result=Dataget_Waxmold.dump(Data)
    except Exception as e:
        Systemp_log(str(e), "get_Waxmold").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify({'data':result}), HTTP_200_OK

@Laser.post('/set_waxmold')
@swag_from('./docs/Laser/set_waxmold.yaml')
def set_waxmold():
    try:
        Waxmold = request.json['Waxmold']
        NameProduct = request.json['NameProduct']
        cursor.execute("UPDATE Serial_laser SET Waxmold = '" + Waxmold + "'where NameProduct ='" + NameProduct + "'")
        conn.commit()
    except Exception as e:
        Systemp_log(str(e), "set_Waxmold").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify('OK'),HTTP_201_CREATED


@Laser.post('/Update_result')
@swag_from('./docs/Laser/Update_result.yaml')
def update_result():
    try:
        MachineNo = request.json['MachineNo']
        NameProduct = request.json['NameProduct']
        Result = request.json['Result']
        TimeOutBarcode=request.json['TimeOutBarcode']
        #row=request.json['row']
        cursor.execute("WITH CTE AS ( SELECT TOP(20) * FROM [QC].[dbo].[Laser] where (MachineNo = '" + MachineNo + "' and NameProduct='" + NameProduct + "' and Result is NULL) ORDER BY TimeOutDMC desc ) UPDATE CTE SET Result = '"+ Result +"',TimeOutBarcode='"+TimeOutBarcode+"'")
        cursor.execute(
            "UPDATE Count_laser SET Count_laser = '0' where MachineNo = '" + MachineNo + "' and NameProduct='" + NameProduct + "'")
        conn.commit()
        cursor.execute(
            "SELECT Count_laser FROM Count_laser where MachineNo = '" + MachineNo + "' and NameProduct='" + NameProduct + "'")
        count = cursor.fetchall()
    except Exception as e:
        Systemp_log(str(e), "update_result").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify(count[0][0]), HTTP_201_CREATED

@Laser.post('/DMC_setup_history')
@swag_from('./docs/Laser/DMC_setup_history.yaml')
def DMC_setup_history():
    try:
        Date = request.json['Date']
        NguoiThayDoi = request.json['NguoiThayDoi']
        MaHang = request.json['MaHang']
        MaBanVeTruoc= request.json['MaBanVeTruoc']
        MaBanVeSau =  request.json['MaBanVeSau']
        PhienBanTruoc = request.json['PhienBanTruoc']
        PhienBanSau = request.json['PhienBanSau']
        cursor.execute(
            '''INSERT INTO [QC].[dbo].[DMC_setup_history] VALUES (?,?,?,?,?,?,?) ''',
            Date,
            NguoiThayDoi,
            MaHang,
            MaBanVeTruoc,
            MaBanVeSau,
            PhienBanTruoc,
            PhienBanSau,
        )
        conn.commit()
    except Exception as e:
        Systemp_log(str(e), "DMC_setup_history").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"),HTTP_201_CREATED

@Laser.get("/DMC_change_history")
@swag_from("./docs/Laser/DMC_change_history.yaml")
def DMC_change_history():
    try:
        cursor.execute("select * FROM DMC_setup_history order by Date desc")
        Data = cursor.fetchall()
        result = Laser_DMC_changes.dump(Data)
    except Exception as e:
        Systemp_log(str(e), "DMC_change_history").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify({'data': result}), HTTP_200_OK

@Laser.get("/Get_user_laser/<string:Password>")
@swag_from("./docs/Laser/Get_user_laser.yaml")
def Get_user_laser(Password):
     # thuc=pd.read_sql("Select*From Serial_laser",conn)
     try:
         cursor.execute("Select Name,Security From QC_user where Password ='"+Password+"'")
         Data = cursor.fetchall()
         result=Users_Laser.dump(Data)
     except Exception as e:
         Systemp_log(str(e), "Get_user_laser").append_new_line()
         return jsonify({"Error": "Invalid request, please try again."})
     return jsonify({'data':result}), HTTP_200_OK

@Laser.get("/Security/<string:IP>")
@swag_from("./docs/Laser/Security.yaml")
def Security(IP):
     # thuc=pd.read_sql("Select*From Serial_laser",conn)
     try:
         cursor.execute("Select count(id) From Security where IP ='"+IP+"'")
         Data = cursor.fetchone()
         if Data[0]==1:
             return jsonify("True"), HTTP_200_OK
         else:
             return jsonify("False"), HTTP_200_OK
     except Exception as e:
         Systemp_log(str(e), "Security").append_new_line()
         return jsonify({"Error": "Invalid request, please try again."})
     # result=Dataget_Laser.dump(Data)

@Laser.get("/Set_Security/<string:IP>")
@swag_from("./docs/Laser/Set_Security.yaml")
def Set_Security(IP):
     # thuc=pd.read_sql("Select*From Serial_laser",conn)
     try:
         cursor.execute("Select count(id) From Security where IP ='" + IP + "'")
         Data = cursor.fetchone()
         if Data[0] == 0:
             cursor.execute( '''INSERT INTO Security VALUES (?) ''',IP)
             cursor.commit()
         else:
             return jsonify("Ma da ton tai")
     except Exception as e:
         Systemp_log(str(e), "Security").append_new_line()
         return jsonify("False")
     return jsonify("True")

     # result=Dataget_Laser.dump(Data)

@Laser.post('/synchronized')
@swag_from('./docs/Laser/synchronized.yaml')
def synchronized():
    try:
        Castingname = request.json['Castingname']
        TimeCasting = request.json['TimeCasting']
        cursor.execute("select TimeCasting  FROM [QC].[dbo].[Castingproduct] where TimeCasting = '"+ TimeCasting+"' and Castingname = '"+ Castingname+"'")
        Data=cursor.fetchall()
        if len(Data)==0:
            cursor.execute('''INSERT INTO [QC].[dbo].[Castingproduct] (Castingname,TimeCasting) VALUES (?,?)''',
                               Castingname,
                               TimeCasting
                                )
            conn.commit()
    except Exception as e:
        Systemp_log(str(e), "synchronized").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"),HTTP_201_CREATED

@Laser.post('/count_history')
@swag_from('./docs/Laser/count_history.yaml')
def count_history():
    try:
        MachineNo = request.json['MachineNo']
        strtoday = request.json['strtoday']
        strnextday = request.json['strnextday']
        Result = request.json['Result']
        cursor.execute("select count(*) from [QC].[dbo].[Laser] where Result = '"+Result+"' and MachineNo = '" + MachineNo + "' and TimeOutBarcode >'" + strtoday + "'and TimeOutBarcode < '" + strnextday+"'")

        Data=cursor.fetchall()
        count=Data[0][0]
    except Exception as e:
        Systemp_log(str(e), "count_history").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify(count),HTTP_201_CREATED

@Laser.post('/get_count_result')
@swag_from('./docs/Laser/get_count_result.yaml')
def get_count_result():
    try:
        MachineNo = request.json['MachineNo']
        NameProduct = request.json['NameProduct']
        cursor.execute(
            "SELECT Count_laser FROM Count_laser where MachineNo = '" + MachineNo + "' and NameProduct='" + NameProduct + "'")
        count = cursor.fetchall()
    except Exception as e:
        Systemp_log(str(e), "get_count_result").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify(count[0][0]), HTTP_201_CREATED

@Laser.post('/Laser_result_history')
@swag_from('./docs/Laser/Laser_result_history.yaml')
def Laser_result_history():
    try:
        MachineNo = request.json['MachineNo']
        NameProduct = request.json['NameProduct']
        Result = request.json['Result']
        cursor.execute(" select top(10)DMCin,Quality,TimeOutBarcode FROM [QC].[dbo].[Laser] where Result='"+Result+"' and MachineNo = '" +MachineNo+ "' and NameProduct = '"+NameProduct+ "' order by TimeOutDMC desc")
        Data=cursor.fetchall()
        result = Result_Lasers.dump(Data)
    except Exception as e:
        Systemp_log(str(e), "Laser_result_history").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify({'data': result}), HTTP_200_OK

@Laser.post('/fill_malo')
@swag_from('./docs/Laser/fill_malo.yaml')
def fill_malo():
    try:
        DMCout = request.json['DMCout']
        NameProduct = request.json['NameProduct']
        cursor.execute("select count(*) from Laser where DMCout like '"+DMCout+"%' and NameProduct = '"+NameProduct+"'")
        Data=cursor.fetchall()
        count=Data[0][0]
    except Exception as e:
        Systemp_log(str(e), "fill_malo").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify(count),HTTP_201_CREATED

@Laser.post('/Laser_all_data')
@swag_from('./docs/Laser/Laser_all_data.yaml')
def Laser_all_data():
    try:
        MachineNo = request.json['MachineNo']
        NameProduct = request.json['NameProduct']
        TimeStart = request.json['TimeStart']
        TimeFinish = request.json['TimeFinish']
        NameOperator = request.json['NameOperator']
        cursor.execute("select * FROM Laser where TimeOutDMC BETWEEN '"+TimeStart+"' AND '"+TimeFinish+"'and NameProduct like '%"+NameProduct+"%' and NameOperator like '%"+NameOperator+"%' and MachineNo like '%"+MachineNo+"%' order by TimeOutDMC desc")
        Data=cursor.fetchall()

        result = Laser_Historys.dump(Data)
        print(result)
    except Exception as e:
        Systemp_log(str(e), "Laser_all_data").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify({'data': result}), HTTP_200_OK

@Laser.get("/Check_castingname/<string:Castingname>")
@swag_from("./docs/Laser/Castingname.yaml")
def Check_castingname(Castingname):
    try:
         cursor.execute("SELECT count(*) From Castingproduct where Castingname='"+Castingname+"'")
         Data = cursor.fetchone()
         if Data[0] == 0:
             return jsonify("False"), HTTP_200_OK
         else:
             return jsonify("True"), HTTP_200_OK
    except Exception as e:
        Systemp_log(str(e), "Check_castingname").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})

@Laser.post('/Type_error')
@swag_from('./docs/Laser/Type_error.yaml')
def Type_error():
    try:
        Status_error = request.json['Status_error']
        cursor.execute("SELECT Type_error FROM Status_Error_Laser WHERE Status_error = N'"+Status_error+"'")
        Data=cursor.fetchall()
    except Exception as e:
        Systemp_log(str(e), "DMC_setup_history").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify(Data[0][0]),HTTP_201_CREATED

@Laser.get("/List_error")
@swag_from("./docs/Laser/List_error.yaml")
def List_error():
    try:
        cursor.execute("SELECT Status_error FROM Status_Error_Laser")
        Data = cursor.fetchall()
        result = Error_Lasers.dump(Data)
    except Exception as e:
        Systemp_log(str(e), "DMC_change_history").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify({'data': result}), HTTP_200_OK

@Laser.post('/SaveData')
@swag_from('./docs/Laser/SaveData.yaml')
def SaveData():
    try:
            MachineNo = request.json['MachineNo']
            NameOperator = request.json['NameOperator']
            NameProduct = request.json['NameProduct']
            DMCin = request.json['DMCin']
            TimeInDMC = request.json['TimeInDMC']
            TimeOutDMC = request.json['TimeOutDMC']
            DMCout = request.json['DMCout']
            TimeOutBarcode = request.json['TimeOutBarcode']
            DMCRework = request.json['DMCRework']
            Result = request.json['Result']
            Quality = request.json['Quality']
            Status = request.json['Status']
            Decode = request.json['Decode']
            Symbol_Contrast = request.json['Symbol_Contrast']
            Modulation = request.json['Modulation']
            Reflectance_Margin = request.json['Reflectance_Margin']
            Fixed_Pattern_Damage = request.json['Fixed_Pattern_Damage']
            Format_Info_Damage = request.json['Format_Info_Damage']
            Version_Info_Damage = request.json['Version_Info_Damage']
            Axial_Nonuniformity = request.json['Axial_Nonuniformity']
            Grid_Nonuniformity = request.json['Grid_Nonuniformity']
            Unused_Err_Correction = request.json['Unused_Err_Correction']
            Print_Growth_Horizontal = request.json['Print_Growth_Horizontal']
            Print_Growth_Vertical = request.json['Print_Growth_Vertical']

            cursor.execute(
                '''INSERT INTO Laser(MachineNo,NameOperator,NameProduct,DMCin,TimeInDMC,TimeOutDMC,DMCout,TimeOutBarcode,DMCRework,Result,Quality,Status,Decode,Symbol_Contrast,Modulation,Reflectance_Margin,Fixed_Pattern_Damage,Format_Info_Damage,Version_Info_Damage,Axial_Nonuniformity,Grid_Nonuniformity,Unused_Err_Correction,Print_Growth_Horizontal,Print_Growth_Vertical) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ''',
                MachineNo,
                NameOperator,
                NameProduct,
                DMCin,
                TimeInDMC,
                TimeOutDMC,
                DMCout,
                TimeOutBarcode,
                DMCRework,
                Result,
                Quality,
                Status,
                Decode,
                Symbol_Contrast,
                Modulation,
                Reflectance_Margin,
                Fixed_Pattern_Damage,
                Format_Info_Damage,
                Version_Info_Damage,
                Axial_Nonuniformity,
                Grid_Nonuniformity,
                Unused_Err_Correction,
                Print_Growth_Horizontal,
                Print_Growth_Vertical
            )
            conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Save_Data").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"), HTTP_201_CREATED

@Laser.get("/Get_machine_laser/<string:DMCin>")
@swag_from("./docs/Laser/Get_machine_laser.yaml")
def Get_machine_laser(DMCin):
    try:
         cursor.execute("select Machineno FROM [QC].[dbo].[Laser] where DMCin like '"+DMCin+"'")
         Data = cursor.fetchall()
         if len(Data)==0:
             return jsonify(" ")
         else:
             return jsonify(Data[0][0].strip())
    except Exception as e:
        Systemp_log(str(e), "Check_castingname").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})

def reset_serial():
     global dt
     while True:
         try:
             format_data = "%y/%m/%d %H:%M:%S"
             if (datetime.datetime.now() - datetime.datetime.strptime(dt+" 00:00:0", format_data)).days >= 1:
                  cursor.execute("UPDATE Serial_laser SET Serial = 1,Time_reset='"+datetime.datetime.now().strftime("%y/%m/%d")+"'")
                  conn.commit()
                  cursor.execute('Select Time_reset From Serial_laser where id=1')
                  dt =cursor.fetchall()[0][0]
             time.sleep(2)
         except Exception as e:
             Systemp_log(str(e), "reset_serial").append_new_line()
reset_serialrun = Thread(target=reset_serial)
reset_serialrun.daemon = True
reset_serialrun.start()



