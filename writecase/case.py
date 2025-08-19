import openpyxl
from openpyxl import load_workbook
import os
import shutil
from typing import Tuple
import pandas as pd

def readexcel(path:str) -> Tuple[openpyxl.Workbook, openpyxl.worksheet.worksheet.Worksheet]:
    # print(f"{path}")
    book = load_workbook(path)
    sheet = book['2.测试明细']
    return book,sheet

def read_signal_excel(path:str, sheet):
    global singals
    singals = pd.read_excel(path, sheet_name=sheet, header=1, dtype=str, engine='openpyxl').iloc[:, 19:22]
    # print(singals)

def readCells(sheet:openpyxl.worksheet.worksheet.Worksheet):
    base = 65 - 1
    for index in range(3,1500):
        if (sheet[f'F{index}'].value == "否"):
            continue
        for cols in range(16, 19):
            #read current statement
            rescell = sheet[f'{chr(base + cols - 3)}{index}']
            if rescell.value != None: 
                continue
            # if none, read the condition
            cells = sheet[f'{chr(base + cols)}{index}'].value
            if cells == None:
                break
            print(f'{chr(base + cols)}{index}')
            # trans condition to out statement
            res_str = ""
            # read by line
            for i, item in enumerate(cells.split('\n'), start=1):
                if item == '-':
                    res_str = item
                    break
                if i > 1:
                    res_str += "\n"
                if " = " in item:
                    msg = find_messgage_label(item)
                    if msg != None:
                        if cols == 18:
                            item = f'检测到：{msg}.{item}'
                            pass
                        else:
                            item = f'发送CAN信号：{msg}.{item}'
                    # print(msg)
                res_str += f'{i}.{item}'
            #save statement
            rescell.value = res_str
            # print(res_str)

def find_messgage_label(item:str) -> str:
    data = item.split(' = ')[0]
    # print(data)
    msg = singals[singals['data label'] == data]['message label  ']
    # print(msg.values)
    return None if msg.values.size == 0 else msg.values[0]
    

if __name__ == "__main__":
    # path = "D:\\DailyWork\\12\\04\\BEV-Step3-CDC(MM)_SQualificationTest_2.11.1_Charging.xlsx"
    path = "D:\\WorkProject\\Mecna\\01_开发库\\21_设计\\02_软件开发\\06_软件合格性测试\\03_测试用例与报告\\机能\\1.1.8_Vehicle\\BEV-Step3-CDC(MM)_SQualificationTest_2.11.1_Charging.xlsx"
    dir = os.path.dirname(path)
    name = os.path.basename(path)
    outdir = "D:\\WorkProject\\Mecna\\01_开发库\\21_设计\\02_软件开发\\06_软件合格性测试\\03_测试用例与报告\\机能\\1.1.8_Vehicle\\"
    outpath = os.path.join(outdir, name)
    signalpath = "D:\\WorkProject\Mecna\\01_开发库\\21_设计\\02_软件开发\\02_软件架构设计\\02_软件架构设计书\\02_HIDL设计\HIDL接口1.0\\Vehicle\\BEV-Step3-CDC(MM)_VehicleHAL_propertyid定义.xlsm"
    sheetname = "SolarCharging&Charging"
    read_signal_excel(signalpath, sheetname)
    book, sheet = readexcel(outpath)
    readCells(sheet)
    book.save(outpath)
    os.startfile(outpath)