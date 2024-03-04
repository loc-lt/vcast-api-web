import pyodbc
from pyodbc import Error
import time
from datetime import datetime
while True:
    try:
        conn = pyodbc.connect(
            'Driver={SQL Server}; Server=LAPTOP-5SUO8BDU\SQLEXPRESS; uid=sa; pwd=1234;Database=thuc; Trusted_Connection=No;')
        cursor = conn.cursor()
        break
    except Error as err:
        print(f"Error1: '{err}'")
        time.sleep(0.5)
def insert(Machineno,Position,Name_product,DMC_Fixture,DMC_product,Machine1,TimeinCNC1,TimeoutCNC1):
    # cursor.execute('INSERT INTO [thuc].[dbo].[CNC_OP1] (Machineno,Position,Name_product,DMC_Fixture,DMC_product,Machine1,TimeinCNC1,TimeoutCNC1) VALUES ( '+list+ ');')

    cursor.execute('''INSERT INTO [thuc].[dbo].[CNC_OP1] (Machineno,Position,Name_product,DMC_Fixture,DMC_product,Machine1,TimeinCNC1,TimeoutCNC1) VALUES (?,?,?,?,?,?,?,?)
                                                            ''',
                               Machineno,
                               Position,
                               Name_product,
                               DMC_Fixture,
                               DMC_product,
                               Machine1,
                               TimeinCNC1,
                               TimeoutCNC1
                               )
    conn.commit()
def update(DMC_product,Machine2,TimeinCNC2,TimeoutCNC2):
    cursor.execute("UPDATE [thuc].[dbo].[CNC_OP1] SET Machine2 = '" + Machine2 + "',TimeinCNC2=")
    conn.commit()