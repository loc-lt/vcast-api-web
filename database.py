from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow,fields
from datetime import datetime
import string
import random
import pyodbc
from pyodbc import Error
import time
ma = Marshmallow()
while True:
    try:
        conn = pyodbc.connect(
            'Driver={SQL Server}; Server=192.168.8.21; uid=sa; pwd=1234;Database=QC; Trusted_Connection=No;')
        cursor = conn.cursor()
        break
    except Error as err:
        print(f"Error1: '{err}'")
        time.sleep(0.5)

    # def __int__(self,Machine,Barcode,Position,Air_value,Time_Start,Time_Finish,Quality):
    #     self.Machine=Machine
    #     self.Barcode=Barcode
    #     self.Position=Position
    #     self.Air_value=Air_value
    #     self.Time_Start=Time_Start
    #     self.Time_Finish=Time_Finish
    #     self.Quality=Quality
# Product Schema
class ProducAirtight(ma.Schema):
    class Meta:
        fields=('id','Machine','Barcode','Position','Air_value','Time_Start','Time_Finish','Quality')
Data_Airtight=ProducAirtight()
Dataget_Airtight=ProducAirtight(many=True)

class ProducLaser(ma.Schema):
    class Meta:
        fields=('id','Serial')
Data_Laser=ProducLaser()
Dataget_Laser=ProducLaser(many=True)

class ProducWaxmoldLaser(ma.Schema):
    class Meta:
        fields=('id','Waxmold')
Data_Waxmold=ProducWaxmoldLaser()
Dataget_Waxmold=ProducWaxmoldLaser(many=True)

class Laser_user(ma.Schema):
    class Meta:
        fields=('Name','Security')
User_Laser=Laser_user()
Users_Laser=Laser_user(many=True)

class Laser_history_result(ma.Schema):
    class Meta:
        fields=('DMCin','Quality','TimeOutBarcode')
Result_Laser=Laser_history_result()
Result_Lasers=Laser_history_result(many=True)

class Laser_DMC_change_history(ma.Schema):
    class Meta:
        fields=('Date','NguoiThayDoi','MaHang','MaBanVeTruoc','MaBanVeSau','PhienBanTruoc','PhienBanSau')
Laser_DMC_change=Laser_DMC_change_history()
Laser_DMC_changes=Laser_DMC_change_history(many=True)

class Laser_error(ma.Schema):
    class Meta:
        fields=('Status_error','Type_error')
Error_Laser=Laser_error()
Error_Lasers=Laser_error(many=True)

class Laser_History_All(ma.Schema):
    class Meta:
        fields=("id","MachineNo",
        "NameOperator",
        "NameProduct",
        "DMCin",
        "TimeInDMC",
        "TimeOutDMC",
        "DMCout",
        "TimeOutBarcode",
        "DMCRework",
        "Result",
        "Status",
        "Quality",
        "Decode",
        "Symbol_Contrast",
        "Modulation",
        "Reflectance_Margin",
        "Fixed_Pattern_Damage",
        "Format_Info_Damage",
        "Version_Info_Damage",
        "Axial_Nonuniformity",
        "Grid_Nonuniformity",
        "Unused_Err_Correction",
        "Print_Growth_Horizontal",
        "Print_Growth_Vertical")
Laser_History=Laser_History_All()
Laser_Historys=Laser_History_All(many=True)

class Get_ScanQR(ma.Schema):
    class Meta:
        fields=('ID','Product','Time_scan_product','Time_scan_tray','DMC_product','DMC_tray','Compare')
Data_QR=Get_ScanQR()
Dataget_QR=Get_ScanQR(many=True)

class ScanQr_Product(ma.Schema):
    class Meta:
        fields=('Product','DMC_product')
Product_QR=ScanQr_Product()
Products_QR=ScanQr_Product(many=True)

class Setting_TV(ma.Schema):
    class Meta:
        fields=('MachineNo','TV_0','TV_Save','TV_Flag','TV_TimeStart')
Setting_TVDB=Setting_TV()
Settings_TVDB=Setting_TV(many=True)




