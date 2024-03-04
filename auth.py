from os import access
from constants.http_status_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
from flask import Blueprint, app, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flasgger import swag_from
from database import *

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('/insert')
@swag_from('./docs/auth/register.yaml')
def register():
    Machine = request.json['Machine']
    Barcode = request.json['Barcode']
    Position = request.json['Position']
    Air_value= request.json['Air_value']
    Quality =  request.json['Quality']
    Time_Start = request.json['Time_Start']
    Time_Finish = request.json['Time_Finish']
    Air = AirTight(Machine=Machine, Barcode=Barcode, Position=Position,Air_value=Air_value,Time_Start=Time_Start,Time_Finish=Time_Finish,Quality=Quality)
    db.session.add(Air)
    db.session.commit()

    # return jsonify({
    #     'message': "User created",
    #     'value': {
    #         'Machine': Machine,'Barcode':Barcode,"Position ":Position ,"Air_value":Air_value,"Quality":Quality
    #     }
    #
    # }), HTTP_201_CREATED
    return product_schema.jsonify(Air)

@auth.get("/show")
@swag_from("./docs/bookmarks/stats.yaml")
def show():
     Data = AirTight.query.all()
     result=products_schema.dump(Data)

    # output = []

    # for i in Data:
    #     data = {}
        # data[' Machine'] = i. Machine
        # data['Barcode'] = i.Barcode
        # data['Position'] = i.Position
        # data['Air_value'] = i.Air_value
        # data[' Time_Start'] = i.Time_Start
        # data['Time_Finish'] = i.Time_Finish
        # data['Quality'] = i.Quality
        # output.append(data)
     print(result)

     return jsonify({'data':result}), HTTP_200_OK

# @auth.get('/token/refresh')
# @jwt_required(refresh=True)
# def refresh_users_token():
#     identity = get_jwt_identity()
#     access = create_access_token(identity=identity)
#
#     return jsonify({
#         'access': access
#     }), HTTP_200_OK
@auth.route("/show1/<string:Machine>", methods=["GET"])
# @auth.get("/show1/Machine")
@swag_from("./docs/auth/login.yaml")
def show1(Machine):
     print(Machine)
     Data1 = AirTight.query.filter(AirTight.Machine==Machine)
     result1 = products_schema.dump(Data1)
     return jsonify({'data':result1}), HTTP_200_OK