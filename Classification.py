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

Classification = Blueprint("Classification", __name__, url_prefix="/api/v1/Classification")

@Classification.post('/Save_Classification')
@swag_from('./docs/Classification/Save_Data.yaml')
def Save_Data_Classification():
    try:
            lazer_machine = request.json['lazer_machine']
            Time_check = request.json['Time_check']
            pallet_num = request.json['pallet_num']
            Num = request.json['Num']
            name = request.json['name']
            total_code = request.json['total_code']
            total_quality = request.json['total_quality']
            dataman_read_matrix_code = request.json['dataman_read_matrix_code']
            dataman_total_quality = request.json['dataman_total_quality']
            dataman_Decode = request.json['dataman_Decode']
            dataman_Symbol_Contrast = request.json['dataman_Symbol_Contrast']
            dataman_Modulation = request.json['dataman_Modulation']
            dataman_Reflectance_Margin = request.json['dataman_Reflectance_Margin']
            dataman_Fixed_Pattern_Damage = request.json['dataman_Fixed_Pattern_Damage']
            dataman_Format_Info_Damage = request.json['dataman_Format_Info_Damage']
            dataman_Version_Info_Damage = request.json['dataman_Version_Info_Damage']
            dataman_Axial_Nonuniformity = request.json['dataman_Axial_Nonuniformity']
            dataman_Grid_Nonuniformity = request.json['dataman_Grid_Nonuniformity']
            dataman_Unused_Err_Correction = request.json['dataman_Unused_Err_Correction']
            dataman_Print_Growth_Horizontal = request.json['dataman_Print_Growth_Horizontal']
            dataman_Print_Growth_Vertical = request.json['dataman_Print_Growth_Vertical']
            camera_matrix_code = request.json['camera_matrix_code']
            camera_pin_1 = request.json['camera_pin_1']
            camera_pin_2 = request.json['camera_pin_2']
            camera_laser_machine = request.json['camera_laser_machine']
            camera_cnc_line_id = request.json['camera_cnc_line_id']
            camera_product_shape = request.json['camera_product_shape']
            camera_dmc_pos_x = request.json['camera_dmc_pos_x']
            camera_dmc_pos_y = request.json['camera_dmc_pos_y']
            error_code = request.json['error_code']
            error_detail = request.json['error_detail']
            note = request.json['note']
            cursor.execute(
                '''INSERT INTO Classification (lazer_machine,Time_check,pallet_num,Num,name,total_code,total_quality,dataman_read_matrix_code,
                dataman_total_quality,dataman_Decode,dataman_Symbol_Contrast,dataman_Modulation,
                dataman_Reflectance_Margin,dataman_Fixed_Pattern_Damage,dataman_Format_Info_Damage,dataman_Version_Info_Damage,
                dataman_Axial_Nonuniformity,dataman_Grid_Nonuniformity,dataman_Unused_Err_Correction,dataman_Print_Growth_Horizontal,
                dataman_Print_Growth_Vertical,camera_matrix_code,camera_pin_1,camera_pin_2,camera_laser_machine,camera_cnc_line_id,camera_product_shape,
                camera_dmc_pos_x,camera_dmc_pos_y,error_code,error_detail,note) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ''',
                lazer_machine,
                Time_check,
                pallet_num,
                Num,
                name,
                total_code,
                total_quality,
                dataman_read_matrix_code,
                dataman_total_quality,
                dataman_Decode,
                dataman_Symbol_Contrast,
                dataman_Modulation,
                dataman_Reflectance_Margin,
                dataman_Fixed_Pattern_Damage,
                dataman_Format_Info_Damage,
                dataman_Version_Info_Damage,
                dataman_Axial_Nonuniformity,
                dataman_Grid_Nonuniformity,
                dataman_Unused_Err_Correction,
                dataman_Print_Growth_Horizontal,
                dataman_Print_Growth_Vertical,
                camera_matrix_code,
                camera_pin_1,
                camera_pin_2,
                camera_laser_machine,
                camera_cnc_line_id,
                camera_product_shape,
                camera_dmc_pos_x,
                camera_dmc_pos_y,
                error_code,
                error_detail,
                note
            )
            conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Save_Data_Classification").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"), HTTP_201_CREATED

@Classification.post('/DATA_CLASSIFICATION')
@swag_from('./docs/Classification/DATA_SAVE_CLASSIFICATION.yaml')
def Data_Save_Classification():
    try:
            lazer_machine = request.json['lazer_machine']
            Time_check = request.json['Time_check']
            pallet_num = request.json['pallet_num']
            Num = request.json['Num']
            name = request.json['name']
            total_code = request.json['total_code']
            total_quality = request.json['total_quality']
            dataman_read_matrix_code = request.json['dataman_read_matrix_code']
            dataman_total_quality = request.json['dataman_total_quality']
            dataman_Decode = request.json['dataman_Decode']
            dataman_Symbol_Contrast = request.json['dataman_Symbol_Contrast']
            dataman_Modulation = request.json['dataman_Modulation']
            dataman_Reflectance_Margin = request.json['dataman_Reflectance_Margin']
            dataman_Fixed_Pattern_Damage = request.json['dataman_Fixed_Pattern_Damage']
            dataman_Format_Info_Damage = request.json['dataman_Format_Info_Damage']
            dataman_Version_Info_Damage = request.json['dataman_Version_Info_Damage']
            dataman_Axial_Nonuniformity = request.json['dataman_Axial_Nonuniformity']
            dataman_Grid_Nonuniformity = request.json['dataman_Grid_Nonuniformity']
            dataman_Unused_Err_Correction = request.json['dataman_Unused_Err_Correction']
            dataman_Print_Growth_Horizontal = request.json['dataman_Print_Growth_Horizontal']
            dataman_Print_Growth_Vertical = request.json['dataman_Print_Growth_Vertical']
            camera_distance_two_pin = request.json['camera_distance_two_pin']
            camera_matrix_code = request.json['camera_matrix_code']
            camera_pin_1 = request.json['camera_pin_1']
            camera_pin_2 = request.json['camera_pin_2']
            camera_laser_machine = request.json['camera_laser_machine']
            camera_cnc_line_id = request.json['camera_cnc_line_id']
            camera_product_shape = request.json['camera_product_shape']
            camera_dmc_pos_x = request.json['camera_dmc_pos_x']
            camera_dmc_pos_y = request.json['camera_dmc_pos_y']
            error_code = request.json['error_code']
            error_detail = request.json['error_detail']
            note = request.json['note']
            cursor.execute(
                '''INSERT INTO Classification (lazer_machine,Time_check,pallet_num,Num,name,total_code,total_quality,dataman_read_matrix_code,
                dataman_total_quality,dataman_Decode,dataman_Symbol_Contrast,dataman_Modulation,
                dataman_Reflectance_Margin,dataman_Fixed_Pattern_Damage,dataman_Format_Info_Damage,dataman_Version_Info_Damage,
                dataman_Axial_Nonuniformity,dataman_Grid_Nonuniformity,dataman_Unused_Err_Correction,dataman_Print_Growth_Horizontal,
                dataman_Print_Growth_Vertical,camera_distance_two_pin,camera_matrix_code,camera_pin_1,camera_pin_2,camera_laser_machine,camera_cnc_line_id,camera_product_shape,
                camera_dmc_pos_x,camera_dmc_pos_y,error_code,error_detail,note) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ''',
                lazer_machine,
                Time_check,
                pallet_num,
                Num,
                name,
                total_code,
                total_quality,
                dataman_read_matrix_code,
                dataman_total_quality,
                dataman_Decode,
                dataman_Symbol_Contrast,
                dataman_Modulation,
                dataman_Reflectance_Margin,
                dataman_Fixed_Pattern_Damage,
                dataman_Format_Info_Damage,
                dataman_Version_Info_Damage,
                dataman_Axial_Nonuniformity,
                dataman_Grid_Nonuniformity,
                dataman_Unused_Err_Correction,
                dataman_Print_Growth_Horizontal,
                dataman_Print_Growth_Vertical,
                camera_distance_two_pin,
                camera_matrix_code,
                camera_pin_1,
                camera_pin_2,
                camera_laser_machine,
                camera_cnc_line_id,
                camera_product_shape,
                camera_dmc_pos_x,
                camera_dmc_pos_y,
                error_code,
                error_detail,
                note
            )
            conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Save_Data_Classification").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"), HTTP_201_CREATED

@Classification.post('/Update_Data')
@swag_from('./docs/Classification/Update_Data.yaml')
def Update_Data_Classification():
    try:
            lazer_machine = request.json['lazer_machine']
            pallet_num = request.json['pallet_num']
            Num = request.json['Num']
            total_code = request.json['total_code']
            dmc_was_replace = request.json['dmc_was_replace']
            total_quality = request.json['total_quality']
            dataman_read_matrix_code = request.json['dataman_read_matrix_code']
            dataman_total_quality = request.json['dataman_total_quality']
            dataman_Decode = request.json['dataman_Decode']
            dataman_Symbol_Contrast = request.json['dataman_Symbol_Contrast']
            dataman_Modulation = request.json['dataman_Modulation']
            dataman_Reflectance_Margin = request.json['dataman_Reflectance_Margin']
            dataman_Fixed_Pattern_Damage = request.json['dataman_Fixed_Pattern_Damage']
            dataman_Format_Info_Damage = request.json['dataman_Format_Info_Damage']
            dataman_Version_Info_Damage = request.json['dataman_Version_Info_Damage']
            dataman_Axial_Nonuniformity = request.json['dataman_Axial_Nonuniformity']
            dataman_Grid_Nonuniformity = request.json['dataman_Grid_Nonuniformity']
            dataman_Unused_Err_Correction = request.json['dataman_Unused_Err_Correction']
            dataman_Print_Growth_Horizontal = request.json['dataman_Print_Growth_Horizontal']
            dataman_Print_Growth_Vertical = request.json['dataman_Print_Growth_Vertical']
            camera_matrix_code = request.json['camera_matrix_code']
            camera_pin_1 = request.json['camera_pin_1']
            camera_pin_2 = request.json['camera_pin_2']
            camera_laser_machine = request.json['camera_laser_machine']
            camera_cnc_line_id = request.json['camera_cnc_line_id']
            camera_product_shape = request.json['camera_product_shape']
            camera_dmc_pos_x = request.json['camera_dmc_pos_x']
            camera_dmc_pos_y = request.json['camera_dmc_pos_y']
            error_code = request.json['error_code']
            error_detail = request.json['error_detail']
            note = request.json['note']
            cursor.execute("Update Classification set lazer_machine='"+lazer_machine+"', total_code='"+total_code+"',"
                           " dmc_was_replace='"+dmc_was_replace+"',total_quality='"+total_quality+"', dataman_read_matrix_code='"+dataman_read_matrix_code+"',"
                            "dataman_total_quality='"+dataman_total_quality+"',dataman_Decode='"+dataman_Decode+"', "
                            "dataman_Symbol_Contrast='"+dataman_Symbol_Contrast+"',dataman_Modulation='"+dataman_Modulation+"',"
                            "dataman_Reflectance_Margin='"+dataman_Reflectance_Margin+"',dataman_Fixed_Pattern_Damage='"+dataman_Fixed_Pattern_Damage+"',"
                          "dataman_Format_Info_Damage='"+dataman_Format_Info_Damage+"',dataman_Version_Info_Damage='"+dataman_Version_Info_Damage+"',"
                           "dataman_Axial_Nonuniformity='"+dataman_Axial_Nonuniformity+"',dataman_Grid_Nonuniformity='"+dataman_Grid_Nonuniformity+"',"
                          "dataman_Unused_Err_Correction='"+dataman_Unused_Err_Correction+"',dataman_Print_Growth_Horizontal='"+dataman_Print_Growth_Horizontal+"',"
                         "dataman_Print_Growth_Vertical='"+dataman_Print_Growth_Vertical+"',camera_matrix_code='"+camera_matrix_code+"',camera_pin_1='"+camera_pin_1+"',"
                        "camera_pin_2='"+camera_pin_2+"',camera_laser_machine='"+camera_laser_machine+"',camera_cnc_line_id='"+camera_cnc_line_id+"',camera_product_shape='"+camera_product_shape+"',"
                        "camera_dmc_pos_x='"+camera_dmc_pos_x+"',camera_dmc_pos_y='"+camera_dmc_pos_y+"',error_code='"+error_code+"',error_detail='"+error_detail+"',note='"+note+"'"
                        "where total_code='"+dmc_was_replace+"' and pallet_num='"+pallet_num+"' and Num='"+Num+"' ")
            conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Update_Data_Classification").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"), HTTP_201_CREATED

@Classification.post('/Update_Data_classification')
@swag_from('./docs/Classification/Update_Data_classification.yaml')
def Update_Data():
    try:
            lazer_machine = request.json['lazer_machine']
            pallet_num = request.json['pallet_num']
            Num = request.json['Num']
            total_code = request.json['total_code']
            dmc_was_replace = request.json['dmc_was_replace']
            total_quality = request.json['total_quality']
            dataman_read_matrix_code = request.json['dataman_read_matrix_code']
            dataman_total_quality = request.json['dataman_total_quality']
            dataman_Decode = request.json['dataman_Decode']
            dataman_Symbol_Contrast = request.json['dataman_Symbol_Contrast']
            dataman_Modulation = request.json['dataman_Modulation']
            dataman_Reflectance_Margin = request.json['dataman_Reflectance_Margin']
            dataman_Fixed_Pattern_Damage = request.json['dataman_Fixed_Pattern_Damage']
            dataman_Format_Info_Damage = request.json['dataman_Format_Info_Damage']
            dataman_Version_Info_Damage = request.json['dataman_Version_Info_Damage']
            dataman_Axial_Nonuniformity = request.json['dataman_Axial_Nonuniformity']
            dataman_Grid_Nonuniformity = request.json['dataman_Grid_Nonuniformity']
            dataman_Unused_Err_Correction = request.json['dataman_Unused_Err_Correction']
            dataman_Print_Growth_Horizontal = request.json['dataman_Print_Growth_Horizontal']
            dataman_Print_Growth_Vertical = request.json['dataman_Print_Growth_Vertical']
            camera_distance_two_pin = request.json['camera_distance_two_pin']
            camera_matrix_code = request.json['camera_matrix_code']
            camera_pin_1 = request.json['camera_pin_1']
            camera_pin_2 = request.json['camera_pin_2']
            camera_laser_machine = request.json['camera_laser_machine']
            camera_cnc_line_id = request.json['camera_cnc_line_id']
            camera_product_shape = request.json['camera_product_shape']
            camera_dmc_pos_x = request.json['camera_dmc_pos_x']
            camera_dmc_pos_y = request.json['camera_dmc_pos_y']
            error_code = request.json['error_code']
            error_detail = request.json['error_detail']
            note = request.json['note']
           
                        
            cursor.execute("Update Classification set lazer_machine='"+lazer_machine+"', total_code='"+total_code+"',"
                           " dmc_was_replace='"+dmc_was_replace+"',total_quality='"+total_quality+"', dataman_read_matrix_code='"+dataman_read_matrix_code+"',"
                            "dataman_total_quality='"+dataman_total_quality+"',dataman_Decode='"+dataman_Decode+"', "
                            "dataman_Symbol_Contrast='"+dataman_Symbol_Contrast+"',dataman_Modulation='"+dataman_Modulation+"',"
                            "dataman_Reflectance_Margin='"+dataman_Reflectance_Margin+"',dataman_Fixed_Pattern_Damage='"+dataman_Fixed_Pattern_Damage+"',"
                          "dataman_Format_Info_Damage='"+dataman_Format_Info_Damage+"',dataman_Version_Info_Damage='"+dataman_Version_Info_Damage+"',"
                           "dataman_Axial_Nonuniformity='"+dataman_Axial_Nonuniformity+"',dataman_Grid_Nonuniformity='"+dataman_Grid_Nonuniformity+"',"
                          "dataman_Unused_Err_Correction='"+dataman_Unused_Err_Correction+"',dataman_Print_Growth_Horizontal='"+dataman_Print_Growth_Horizontal+"',"
                         "dataman_Print_Growth_Vertical='"+dataman_Print_Growth_Vertical+"',camera_distance_two_pin='"+camera_distance_two_pin+"',camera_matrix_code='"+camera_matrix_code+"',camera_pin_1='"+camera_pin_1+"',"
                        "camera_pin_2='"+camera_pin_2+"',camera_laser_machine='"+camera_laser_machine+"',camera_cnc_line_id='"+camera_cnc_line_id+"',camera_product_shape='"+camera_product_shape+"',"
                        "camera_dmc_pos_x='"+camera_dmc_pos_x+"',camera_dmc_pos_y='"+camera_dmc_pos_y+"',error_code='"+error_code[2:-2]+"',error_detail='"+error_detail[2:-2]+"',note='"+note+"'"
                        "where total_code='"+dmc_was_replace+"' and pallet_num='"+pallet_num+"' and Num='"+Num+"' ")
            conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Update_Data_Classification").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
        
    return jsonify("OK"), HTTP_201_CREATED

@Classification.post('/Save_Pallet_Classification')
@swag_from('./docs/Classification/Save_Pallet.yaml')
def Save_Pallet_Classification():
    try:
            Time = request.json['Time']
            Product = request.json['Product']
            Date = request.json['Date']
            Pallet_No = request.json['Pallet_No']
            Pallet_Name = request.json['Pallet_Name']
            SPLR_LOT_NO = request.json['SPLR_LOT_NO']

            cursor.execute(
                '''INSERT INTO Pallet (Time,Product,Date,Pallet_No,Pallet_Name,SPLR_LOT_NO) VALUES (?,?,?,?,?,?) ''',
                Time,
                Product,
                Date,
                Pallet_No,
                Pallet_Name,
                SPLR_LOT_NO
            )
            conn.commit()
    except Exception as e:
        Systemp_log(str(e), "Save_Pallet_Classification").append_new_line()
        return jsonify({"Error": "Invalid request, please try again."})
    return jsonify("OK"), HTTP_201_CREATED

