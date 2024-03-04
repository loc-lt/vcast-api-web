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
senderrorcnc = Blueprint("senderrorcnc", __name__, url_prefix="/api/v1/senderrorcnc")

def senderror(msg):
    try:
        list_id = [-4025240473]
          
        for id in list_id:
            to_url = 'https://api.telegram.org/bot1823472278:AAEup_6eYPpCcU5uJH_v2o0jdzBGDMDnPBw/sendMessage'
            paremeters = {
                "chat_id": id,
                "text": msg
            }
            resp = requests.get(to_url, data=paremeters)
    except Exception as e:
        Systemp_log(str(e), "Request").append_new_line()
        pass

@senderrorcnc.post('/send_message')
@swag_from('./docs/Errorcnc/Sendmessage.yaml')
def sendtelegram():
    SET = request.json['SET']
    MSG = request.json['MSG']
    POS = request.json['POS']
    cursor.execute("  select b.Line from [BonusCalculation].[dbo].[Machine_History] a, [BonusCalculation].[dbo].[Machine_CNC] b, [BonusCalculation].[dbo].[Worker_Manager] c where  b.Machineno= '"+SET+"' and b.Pos_product='"+POS+"'")
    data=cursor.fetchall()
    if len(data)>0:
        senderror(MSG+" Line "+data[0][0])
        return jsonify("ok")
    return jsonify("false")
