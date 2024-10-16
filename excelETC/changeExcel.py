import pandas as  pd
import xlwings as xw
from tkinter import filedialog
import tkinter

def pandasRead():
    global src_df, dst_df
    src_df = pd.read_excel(io=src_path, sheet_name=src_sh, engine='openpyxl', header=2)
    dst_df = pd.read_excel(io=dst_path, sheet_name=dst_sh, engine='openpyxl', header=2)
    print("_______read done___________________")

def xlwingsRead():
    global wb,ws
    wb = xw.Book(dst_path)
    ws = wb.sheets[dst_sh]

def selectFile():
    global src_path,dst_path
    # src_path = filedialog.askopenfilename()
    # print(src_path)
    # dst_path = filedialog.askopenfilename()
    # print(dst_path)
    src_path = "D:/DailyWork/12/18/24MM 09_04_01_Spec_Charging Function_要件分析.xlsx"
    # dst_path = "D:/DailyWork/12/18/丰田_24MM_SArchitectureDesign_2.11.2_Solar Charging.xlsx"
    dst_path = "D:/DailyWork/12/18/丰田_24MM_SArchitectureDesign_2.11.1_Charging.xlsx"

def readRows(df, value):
    rows = df[df.apply(lambda row: row.astype(str).str.contains(str(value)).any(), axis=1)]
    return rows

def readValue(value, line):
    rows = readRows(value)
    if line == "设置值":
        return str(int(rows[line].values[0]))
    return rows[line].values[0]

def readRef():
    path = "D:/DailyWork/12/18/SWE.1-SWE.2 Trace Check_NC.xlsx"
    sh = "2.软件需求一览"
    df = pd.read_excel(io=path, sheet_name=sh, engine='openpyxl', header=2, usecols=['模块功能ID'])
    df['模块功能ID'] = df["模块功能ID"].astype(str)
    list = df["模块功能ID"].tolist()
    return list


def setExcel(item):
    # 读取源路径的项的行和列
    print(src_df.loc[src_df[src_indexcol].str.lower() == item.lower()])
    result_src = src_df.loc[src_df[src_indexcol].str.lower() == item.lower()]
    if result_src.empty:
        return
    r = result_src.index[0] + 2
    c = src_df.columns.get_loc(src_indexcol)+1
    print(f"{item} {r}  {c} {src_df.iloc[r-2][c-1]}")
    print(f"{src_df.loc[r, src_col]}")
    print(f"{src_df.loc[c, src_col]}")
    # 读取目标路径的项的行和列
    print(dst_df.loc[dst_df[dst_indexcol].str.lower() == item.lower()])
    r_tar = dst_df.loc[dst_df[dst_indexcol].str.lower() == item.lower()].index[0] + 2
    c_tar = dst_df.columns.get_loc(dst_col) + 1
    print(f"{item} {r_tar}  {c_tar} {dst_df.iloc[r_tar-2][c_tar-1]}")
    print(f"{dst_df.loc[r_tar, dst_col]}")
    print(f"{dst_df.loc[c_tar, dst_col]}")
    value = str(src_df.loc[r, src_col])
    print(value)
    xlwingsRead()
    # edit cell
    cell = ws.range(r_tar, c_tar)
    cell.value = value
    wb.save(dst_path)
    wb.app.quit()
    # pandasRead()

def mainWindow():
    window = tkinter.Tk()
    window.geometry("1000x800")
    
    label_source = tkinter.Label(window, text="source")
    label_source.place(relheight=0.05, relwidth= 0.1, relx=0.01, rely=0)
    text_source = tkinter.Entry(window)
    text_source.place(relheight=0.05, relwidth=0.15, relx=0.11, rely=0)

if __name__ == "__main__" :
    global src_sh, src_col, src_indexcol
    src_col = "系统需求版本"    
    src_sh = "要件分析"
    src_indexcol = "模块功能ID"
    global dst_sh, dst_col, dst_indexcol
    dst_col = "软件规格说明书版本"
    dst_sh = "2.软件需求一览"
    dst_indexcol = "模块功能ID"
    selectFile()
    pandasRead()
    list = readRef()
    for item in list:
        print(item)
        setExcel(item)
