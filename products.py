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
import pandas as pd
import traceback
from flask import session
from flask import *
import numpy as np
import math
import io


products = Blueprint("products", __name__, url_prefix="/api/v1/products")

# COATING
@products.post('/coating')
@swag_from('./docs/products/coating/coating_data.yaml')
def get_coating_data():
    try:
        # Tạo cusor để kết nối với database
        conn = pyodbc.connect('Driver={SQL Server}; Server=192.168.8.21; uid=sa; pwd=1234; Database=Auto; Trusted_Connection=No;', timeout=1)
        cursor = conn.cursor()

        # Lấy dữ liệu coat_name
        coat_name = request.json['coatName']

        # Lấy dữ liệu datetime_start, datetime_end, location
        day_start = request.json['dayStart']
        day_end = request.json['dayEnd']
        time_start = request.json['timeStart']
        time_end = request.json['timeEnd']  

        datetime_start = day_start + " " + time_start
        datetime_end = day_end + " " + time_end

        cursor.execute("SELECT Top(15000)* FROM [Auto].[dbo].[Product_Quantity_W5_"+coat_name+"] where DateTime >'"+datetime_start+"' and DateTime <'"+datetime_end+"'")
        all_records = cursor.fetchall()

        # Lấy số dượng lượng record
        num_records = len(all_records)

        # Nếu lấy dữ liệu ra trống
        if all_records == None:
            ret = {
                'status':False,
                'message':'Not Exist Data'
            }
            return jsonify(ret),400

        # Nếu có máy
        ret ={
                'status':True,
                'message':'Success',
                'data':{}
            }
        
        if num_records == 0:
            ret['data'] = None
            return jsonify(ret)
        
        # Khởi tạo các list dữ liệu cần thiết để vẽ chart
        ret['data']['datetime'] = []
        ret['data']['averageTempList'] = []
        ret['data']['averageHumidList'] = []

        # Lấy averageTempList, averageHumidList
        cursor.execute("select Datetime, average_temp1, average_humid1 from data_"+coat_name+"_W5 where Datetime >'"+datetime_start+"' and Datetime <'"+datetime_end+"' order by Datetime desc")
        temp_humid_average_data = cursor.fetchall()

        for item in temp_humid_average_data:
            datetime_data, average_temp, average_humid = item
            
            ret['data']['datetime'].append(datetime_data.strftime("%Y-%m-%d %H:%M:%S.%f"))
            ret['data']['averageTempList'].append(average_temp)
            ret['data']['averageHumidList'].append(average_humid)

        # Lấy các biến temp_min, temp_max, humid_min, humid_max
        cursor.execute("select * from [Auto].[dbo].[Settinglimitcoatingx5] where Coating = '"+coat_name+"'")
        figues = cursor.fetchone()

        print(figues)

        coating_name, temp_min, temp_max, humid_min, humid_max, layer = figues

        ret['data']['tempMin'] = temp_min
        ret['data']['tempMax'] = temp_max
        ret['data']['humidMin'] = humid_min
        ret['data']['humidMax'] = humid_max

        return jsonify(ret)
    except Exception as e:
        ret = {
            'status':False,
            'message': str(e)
        }
        Systemp_log(traceback.format_exc(), "dmc_data").append_new_line()
        return jsonify(ret),500
    
@products.post('/coating/download')
@swag_from('./docs/products/coating/coating_download.yaml')
def download_coating_data():
    try:
        # Tạo cusor để kết nối với database
        conn = pyodbc.connect('Driver={SQL Server}; Server=192.168.8.21; uid=sa; pwd=1234; Database=Auto; Trusted_Connection=No;', timeout=1)
        cursor = conn.cursor()

        # Lấy dữ liệu time_start, time_end
        time_start = request.json['timeStart']
        time_end = request.json['timeEnd']  

        df1 = pd.read_sql("SELECT * FROM [Auto].[dbo].[Product_Quantity_W5_Coating1] where DateTime >'"+time_start+"' and DateTime <'"+time_end+"'", conn)
        df2 = pd.read_sql("SELECT * FROM [Auto].[dbo].[Product_Quantity_W5_Coating2] where DateTime >'"+time_start+"' and DateTime <'"+time_end+"'", conn)
        df3 = pd.read_sql("SELECT * FROM [Auto].[dbo].[Product_Quantity_W5_Coating3] where DateTime >'"+time_start+"' and DateTime <'"+time_end+"'", conn)
        df4 = pd.read_sql("SELECT * FROM [Auto].[dbo].[Product_Quantity_W5_Coating4] where DateTime >'"+time_start+"' and DateTime <'"+time_end+"'", conn)
        df5 = pd.read_sql("SELECT * FROM [Auto].[dbo].[Product_Quantity_W5_Coating5] where DateTime >'"+time_start+"' and DateTime <'"+time_end+"'", conn)
        df6 = pd.read_sql("SELECT * FROM [Auto].[dbo].[Product_Quantity_W5_Coating6] where DateTime >'"+time_start+"' and DateTime <'"+time_end+"'", conn)

        # Nếu lấy dữ liệu ra trống
        if len(df1) == 0 and len(df2) == 0 and len(df3) == 0 and len(df4) == 0 and len(df5) == 0 and len(df6) == 0:
            ret = {
                'status':False,
                'message':'Not Exist Data'
            }
            return jsonify(ret),400

        output = io.BytesIO()
        writer = pd.ExcelWriter(
            output,
            engine='xlsxwriter')    # add a sheet
        
        df1.index+=1
        df2.index+=1
        df3.index+=1
        df4.index+=1
        df5.index+=1
        df6.index+=1
        df1.to_excel(writer, sheet_name='layer1')
        df2.to_excel(writer, sheet_name='layer2')
        df3.to_excel(writer, sheet_name='layer3')
        df4.to_excel(writer, sheet_name='layer4')
        df5.to_excel(writer, sheet_name='layer5')
        df6.to_excel(writer, sheet_name='layer6')

        # add headers
        writer.close()
        output.seek(0)
        
        return Response(output, mimetype="application/ms-excel",
                    headers={"Content-Disposition": "attachment;filename=Coating_Data.xls"})
    except Exception as e:
        ret = {
            'status':False,
            'message': str(e)
        }
        Systemp_log(traceback.format_exc(), "dmc_data").append_new_line()
        return jsonify(ret),500
    
@products.post('/coating/temp_humid_download')
@swag_from('./docs/products/coating/temp_humid_download.yaml')
def download_temp_humid_data():
    global coat_name
    try:
        # Tạo cusor để kết nối với database
        conn = pyodbc.connect('Driver={SQL Server}; Server=192.168.8.21; uid=sa; pwd=1234; Database=Auto; Trusted_Connection=No;', timeout=1)
        cursor = conn.cursor()

        # Lấy dữ liệu time_start, time_end
        time_start = request.json['timeStart']
        time_end = request.json['timeEnd']

        # Lấy dữ liệu coat_name
        coat_name = request.json['coatName']

        # Lấy coat_data
        cursor.execute("select * from data_"+coat_name+"_W5 where Datetime >'"+time_start+"' and Datetime <'"+time_end+"'")
        coat_data = cursor.fetchall()

        # Lấy coat_data_sorted
        cursor.execute("select Datetime, average_temp1, average_humid1 from data_"+coat_name+"_W5 where Datetime >'"+time_start+"' and Datetime <'"+time_end+"' order by Datetime desc")
        coat_data_sorted = cursor.fetchall()

        # Nếu lấy dữ liệu ra trống
        if coat_data == None:
            ret = {
                'status':False,
                'message':'Not Exist Data'
            }
            return jsonify(ret),400
        
        # Lấy df để lưu dữ liệu vô worksheet
        df_coat_data = pd.read_sql("select * from data_"+coat_name+"_W5 where Datetime >'"+time_start+"' and Datetime <'"+time_end+"'", conn)

        # Nếu có máy
        ret = {
                'status':True,
                'message':'Success',
                'data':{}
            }
        
        # Nếu dữ liệu rỗng
        if len(coat_data) == 0:
            ret['data'] = None
            return jsonify(ret)

        # Khởi tạo các list dữ liệu cần thiết để vẽ chart
        ret['data']['datetime'] = []
        ret['data']['averageTempList'] = []
        ret['data']['averageHumidList'] = []

        for item in coat_data_sorted:
            datetime_data, average_temp, average_humid = item
            
            ret['data']['datetime'].append(datetime_data.strftime("%Y-%m-%d %H:%M:%S.%f"))
            ret['data']['averageTempList'].append(average_temp)
            ret['data']['averageHumidList'].append(average_humid)

        # Lấy các biến temp_min, temp_max, humid_min, humid_max
        cursor.execute("select * from [Auto].[dbo].[Settinglimitcoatingx5] where Coating = '"+coat_name+"'")
        figues = cursor.fetchone()

        coating_name, temp_min, temp_max, humid_min, humid_max, layer = figues

        ret['data']['tempMin'] = temp_min
        ret['data']['tempMax'] = temp_max
        ret['data']['humidMin'] = humid_min
        ret['data']['humidMax'] = humid_max

        image_path = 'static/images/'+coat_name+'.png'
                             
        output = io.BytesIO()
        writer = pd.ExcelWriter(output,engine='xlsxwriter')    # add a sheet
        df_coat_data.index+=1
        df_coat_data.to_excel(writer, sheet_name=str(coat_name))
        worksheet = writer.book.add_worksheet("Chart")

        # Get the xlsxwriter workbook and worksheet objects for the new sheet.
        worksheet.insert_image('A1', image_path, {'x_offset': 15, 'y_offset': 10})

        # add headers
        writer.close()
        output.seek(0)
        
        return Response(output, mimetype="application/ms-excel",
                        headers={"Content-Disposition": "attachment;filename=Temp_Humid_Coating.xls"})
    except Exception as e:
        ret = {
            'status':False,
            'message': str(e)
        }
        Systemp_log(traceback.format_exc(), "temp_humid_download").append_new_line()
        return jsonify(ret),500
    
# SHOT BLASING
@products.post('/shot_blasting')
@swag_from('./docs/products/shot_blasting/shot_blasting_data.yaml')
def get_shot_blasting_data():
    try:
        # Tạo cusor để kết nối với database
        conn = pyodbc.connect('Driver={SQL Server}; Server=192.168.8.21; uid=sa; pwd=1234; Database=Auto; Trusted_Connection=No;', timeout=1)
        cursor = conn.cursor()

        # Lấy dữ liệu datetime_start, datetime_end, location
        day_start = request.json['dayStart']
        day_end = request.json['dayEnd']
        time_start = request.json['timeStart']
        time_end = request.json['timeEnd']

        datetime_start = day_start + " " + time_start
        datetime_end = day_end + " " + time_end

        # Lấy dữ liệu bảng ShotBlasting
        cursor.execute("SELECT Top(15000)* FROM [Auto].[dbo].[ShotBlasting] where Time_Take_out >'"+datetime_start+"' and Time_Take_out <'"+datetime_end+"'")
        all_records = cursor.fetchall()

        # Lấy số dượng lượng record
        num_records = len(all_records)

        # Nếu lấy dữ liệu ra trống
        if all_records == None:
            ret = {
                'status':False,
                'message':'Not Exist Data'
            }
            return jsonify(ret),400

        # Nếu có máy
        ret = {
                'status':True,
                'message':'Success',
                'data':{}
            }
        
        if num_records == 0:
            ret['data'] = None
            return jsonify(ret)
        
        # Nếu lấy dữ liệu không trống        
        # Khởi tạo 2 list dữ liệu cần thiết show bảng dữ liệu và dữ liệu đã qua xử lý để vẽ chart
        ret['data']['table'] = []
        ret['data']['chart'] = {}

        # Lấy dữ liệu để show bảng
        for item in all_records:
            id, machine_no, face, time_set, time_put_into, time_start_temp, time_finish_temp, time_take_out = item
            
            ret['data']['table'].append({
                'id': id,
                'machineNo': machine_no,
                'face': face,
                'timeSet': time_set,
                'timePutInto': time_put_into,
                'timeStart': time_start_temp,
                'timeFinish': time_finish_temp,
                'timeTakeOut': time_take_out
            })

        # Lấy dữ liệu để vẽ chart
        shot_blasting_df = pd.read_sql("SELECT left(Time_Take_out,11) as 'Time', MachineNo, COUNT(MachineNo) AS 'Count'FROM [Auto].[dbo].[ShotBlasting] where Time_Take_out >'"+datetime_start+"' and Time_Take_out <'"+datetime_end+"' GROUP BY left(Time_Take_out,11),MachineNo order by left(Time_Take_out,11) desc", conn)
        
        shot_blasting_df = shot_blasting_df.pivot_table(index='Time', columns='MachineNo')

        # Khảo sát dữ liệu trong df
        print(shot_blasting_df.head(10))
        print(shot_blasting_df.columns.to_list())
        print(shot_blasting_df.values)
        print(shot_blasting_df.index.to_list())

        # Khởi tạo các list dữ liệu để vẽ chart
        ret['data']['chart']['machineNo'] = []
        ret['data']['chart']['timeIndex'] = []
        ret['data']['chart']['machineNoData'] = {}

        # Lấy dữ liệu machine_no
        for item in shot_blasting_df.columns.to_list():
            ret['data']['chart']['machineNo'].append(item[1])

        # Lấy dữ liệu timeIndex
        ret['data']['chart']['timeIndex'] = shot_blasting_df.index.to_list()

        # Lấy dữ liệu machineNoData
        # Khởi tạo các list chứa dữ liệu 
        machine_no_list = ret['data']['chart']['machineNo']
        for item in machine_no_list:
            ret['data']['chart']['machineNoData'][item] = []

        # Add data
        for row_data in shot_blasting_df.values:
            for idx, element in enumerate(row_data):
                ret['data']['chart']['machineNoData'][machine_no_list[idx]].append(element)        

        return jsonify(ret)
    except Exception as e:
        ret = {
            'status':False,
            'message': str(e)
        }
        Systemp_log(traceback.format_exc(), "shot_blasting_data").append_new_line()
        return jsonify(ret),500
    
@products.post('/shot_blasting/download')
@swag_from('./docs/products/shot_blasting/shot_blasting_download.yaml')
def download_shot_blasting_data():
    try:
        # Tạo cusor để kết nối với database
        conn = pyodbc.connect('Driver={SQL Server}; Server=192.168.8.21; uid=sa; pwd=1234; Database=Auto; Trusted_Connection=No;', timeout=1)

        # Lấy dữ liệu time_start, time_end
        time_start = request.json['timeStart']
        time_end = request.json['timeEnd']

        print("SELECT*From[Auto].[dbo].[ShotBlasting] where Time_Take_out >'"+time_start+"' and Time_Take_out <'"+time_end+"'")
        shot_blasting_df = pd.read_sql("SELECT*From[Auto].[dbo].[ShotBlasting] where Time_Take_out >'"+time_start+"' and Time_Take_out <'"+time_end+"'", conn)

        # Nếu lấy dữ liệu ra trống
        if len(shot_blasting_df) == 0:
            ret = {
                'status':False,
                'message':'Not Exist Data'
            }
            return jsonify(ret),400

        output = io.BytesIO()
        writer = pd.ExcelWriter(
            output,
            engine='xlsxwriter')    # add a sheet
        
        shot_blasting_df.to_excel(writer, sheet_name='ShotBlasting', index=False)

        # add headers
        writer.close()
        output.seek(0)
        
        return Response(output, mimetype="application/ms-excel",
                        headers={"Content-Disposition": "attachment;filename=ShotBlasting_Data.xls"})
    except Exception as e:
        ret = {
            'status':False,
            'message': str(e)
        }
        Systemp_log(traceback.format_exc(), "shot_blasting_download").append_new_line()
        return jsonify(ret),500