from os import access
from constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
from flask import Blueprint, app, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flasgger import swag_from
from database import *
from ERROR import *
import requests
import datetime
Kiemtrabot = Blueprint("Kiemtrabot", __name__, url_prefix="/api/v1/Kiemtrabot")
list1 = "-764847888"
list2 ="-893582565"
def senderror(id, msg):
    try:
        to_url = 'https://api.telegram.org/bot1823472278:AAEup_6eYPpCcU5uJH_v2o0jdzBGDMDnPBw/sendMessage'
        paremeters = {
            "chat_id": id,
            "text": msg
        }
        resp = requests.get(to_url, data=paremeters)
    except Exception as e:
        Systemp_log(str(e), "Request").append_new_line()
        pass
def ChangeName(Name):
    try:
        NameProduct = chr(int(Name[0] % 256)) + chr(
            int((Name[0] - Name[0] % 256) / 256)) + chr(
            int(Name[1] % 256)) + chr(int((Name[1] - Name[1] % 256) / 256)) + chr(
            int(Name[2] % 256)) + chr(int((Name[2] - Name[2] % 256) / 256)) + chr(
            int(Name[3] % 256)) + chr(int((Name[3] - Name[3] % 256) / 256))+ chr(
            int(Name[4] % 256)) + chr(int((Name[4] - Name[4] % 256) / 256))
        # + chr(
            # int(Name[5] % 256)) + chr(int((Name[5] - Name[5] % 256) / 256))+ chr(
            # int(Name[6] % 256)) + chr(int((Name[6] - Name[6] % 256) / 256))+ chr(
            # int(Name[7] % 256)) + chr(int((Name[7] - Name[7] % 256) / 256))+ chr(
            # int(Name[8] % 256)) + chr(int((Name[8] - Name[8] % 256) / 256))+ chr(
            # int(Name[9] % 256)) + chr(int((Name[9] - Name[9] % 256) / 256))
        return NameProduct
    except Exception as e:
        Systemp_log(str(e), "Name_send").append_new_line()
        pass
@Kiemtrabot.post('/send_data')
@swag_from('./docs/KTBOT/Senddata.yaml')
def sendtelegram():
    Barcode1 = request.json['Barcode1']
    Barcode2 = request.json['Barcode2']
    Barcode3 = request.json['Barcode3']
    Barcode4= request.json['Barcode4']
    Barcode5 =  request.json['Barcode5']
    # Barcode6 = request.json['Barcode6']
    # Barcode7 = request.json['Barcode7']
    # Barcode8 = request.json['Barcode8']
    # Barcode9 = request.json['Barcode9']
    # Barcode10 = request.json['Barcode10']
    Value = request.json['Value']
    today = datetime.datetime.now()
    strtoday = today.strftime("%Y-%m-%d %H:%M:%S")
    # Barcode = ChangeName(
    #     [int(Barcode1), int(Barcode2), int(Barcode3), int(Barcode4), int(Barcode5), int(Barcode6), int(Barcode7),
    #      int(Barcode8), int(Barcode9), int(Barcode10)])
    Barcode=ChangeName([int(Barcode1),int(Barcode2),int(Barcode3),int(Barcode4),int(Barcode5)])
    msg= "Bacode: "+str(Barcode)+ "  Value:  "+str(float(Value)/100)+"  Time: " +strtoday
    print(msg)
    senderror(list1,msg)
    return jsonify("ok")

@Kiemtrabot.post('/send_error')
@swag_from('./docs/KTBOT/Senderorr.yaml')
def sendtelegramerorcoating():
    ID = request.json['ID']
    MSG = request.json['MSG']
    senderror(ID,MSG)
    return jsonify("ok")
