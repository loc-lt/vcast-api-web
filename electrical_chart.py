path = r"C:\Users\Administrator\Desktop\loclt\QC_Repair\test\VC-PC0277 (Ver 1.1) TIEU CHUAN DAO CU-A1811036-240119-OP10-MC16.xlsx"

# Lấy tên máy
if len(path.split('OP')) == 2:
    machine_name = path.split('OP')[1].split('-')[1].split('.')[0]
else:
    machine_name = path.split('OP')[2].split('-')[1].split('.')[0]

# Đưa đường dẫn file vào
workbook = load_workbook(path)
sheet = workbook.active

for sheet_name in workbook.sheetnames:
    # Lấy DMC_Product
    dmc_product_text = sheet.cell(row=4,column=1).value
    dmc_product = dmc_product_text.split()[2]

    row = 7
    sheet = workbook[sheet_name]
    while True:
        # Lấy các giá trị
        tool_holder = sheet.cell(row=row,column=2).value

        if tool_holder is None:
            break
        elif tool_holder == 'N/A':
            tool_holder = '0'
        else:
            print(tool_holder.split('T'))
            tool_holder = tool_holder.split('T')[1]
            if '(' in tool_holder:
                tool_holder = tool_holder.split('(')[0]

        tool_type = sheet.cell(row=row,column=4).value
        arbor_type = sheet.cell(row=row,column=8).value
        
        # Out while nếu tool_type là None
        if tool_type is None:
            break

        # Lấy tool 
        tool_useage_to_check = sheet.cell(row=row,column=13).value
        
        print(tool_useage_to_check)
        if isinstance(tool_useage_to_check, int):
            tool_useage = tool_useage_to_check
        else:
            if len(tool_useage_to_check.split(":")) > 1:
                if len(tool_useage_to_check.split(":")) == 2:
                    if ')' in tool_useage_to_check.split(":")[1]:
                        tool_useage = tool_useage_to_check.split(":")[1].replace(')', '')
                    else:
                        tool_useage = tool_useage_to_check.split(":")[1]
                elif len(tool_useage_to_check.split(":")) == 3:
                    if ":" in tool_useage_to_check.split()[2]:
                        tool_useage = tool_useage_to_check.split()[2][1:]
                    else:
                        tool_useage = tool_useage_to_check.split()[2]
                else:
                    if 'PCS' in tool_useage_to_check.split(":")[1].split("\n")[0].strip():
                        tool_useage = tool_useage_to_check.split(":")[1].split("\n")[0].strip().replace(' PCS', '')
                    else:
                        tool_useage = tool_useage_to_check.split(":")[1].split("\n")[0].strip()
            else:
                tool_useage = 0

        diameter_tolerance = sheet.cell(row=row,column=16).value
        diameter_tolerance = diameter_tolerance.split('+')

        diameter = diameter_tolerance[0]
        tolerance = diameter_tolerance[1]

        op = sheet_name
        
        print((machine_name, dmc_product, op, tool_type, tool_holder, arbor_type, tool_useage, diameter, tolerance))

        cursor.execute( 
                '''INSERT INTO Bom VALUES (?,?,?,?,?,?,?,?,?) ''',
                    machine_name,
                    dmc_product,
                    op,
                    tool_type, 
                    tool_holder,
                    arbor_type, 
                    tool_useage,
                    diameter,
                    tolerance
            )
        cursor.commit()
        
        row+=1