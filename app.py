from flask.json import jsonify
from constants.http_status_code import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from flask import Flask, config, redirect
import os
import urllib.parse
from Airtight import Airtight
from Laser import Laser
from CNC import CNC
from Casting import Casting
from Coating import Coating
from Measure_Diameter import Measure_Diameter
from Classification import Classification
from thread_verification import ThreadVerification
from database import*
from flask_jwt_extended import JWTManager
from flasgger import Swagger, swag_from
from config.swagger import template, swagger_config
from flask_cors import CORS
from ScanQR import ScanQR
from Sendnongdo import Kiemtrabot
from DONG_BIN import DONGBIN
from electric import Elec
from Tiltmeasurement import TiltMeasurement
from CMM import CMM
from SenderrorCNC import senderrorcnc
from Machine_History import Machine_History
from QC import QC
from Bavia import Bavia
from TayRua import TayRua
from Manager import Manager
from temp_humid import TH
from Scan_Repair_Data import Scan_Repair_Data
from temphumid import temphumid
from electrical import electrical_root
from heat_treatment import heat_treatment
from chemical import chemical
from lwm import lwm
from products import products

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
            SWAGGER={
                'title': "Bookmarks API",
                'uiversion': 3
            }
        )

ma.app=app
ma.init_app(app)
JWTManager(app)
CORS(app)

app.register_blueprint(Airtight)
app.register_blueprint(Laser)
app.register_blueprint(Classification)
app.register_blueprint(CNC)
app.register_blueprint(Casting)
app.register_blueprint(ScanQR)
app.register_blueprint(Coating)
app.register_blueprint(Measure_Diameter)
app.register_blueprint(ThreadVerification)
app.register_blueprint(Kiemtrabot)
app.register_blueprint(DONGBIN)
app.register_blueprint(TiltMeasurement)
app.register_blueprint(Elec)
app.register_blueprint(CMM)
app.register_blueprint(senderrorcnc)
app.register_blueprint(Machine_History)
app.register_blueprint(QC)
app.register_blueprint(Bavia)
app.register_blueprint(TayRua)
app.register_blueprint(Manager)
app.register_blueprint(TH)
app.register_blueprint(Scan_Repair_Data)
app.register_blueprint(temphumid)
app.register_blueprint(electrical_root)
app.register_blueprint(heat_treatment)
app.register_blueprint(chemical)
app.register_blueprint(lwm)
app.register_blueprint(products)
Swagger(app, config=swagger_config, template=template)

@app.errorhandler(HTTP_404_NOT_FOUND)
def handle_404(e):
    return jsonify({'error': 'Not found'}), HTTP_404_NOT_FOUND
@app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
def handle_500(e):
    return jsonify({'error': 'Something went wrong, we are working on it'}), HTTP_500_INTERNAL_SERVER_ERROR

# def create_app(test_config=None):
    # return app
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)