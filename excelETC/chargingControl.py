import pandas as pd
import xlwings as xw
import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import queue
import time
import os
from tkinter import filedialog

panelNameList = ["charging control","schedule charging","optimum charging","optimum plans1","optimum plans2",
                 "current&limit","charing power","limit&battery","supply setting","charge lid"]
controlList = ["P_OCTID", "PCNOWDSP","P_NCTYP","P_NCSTM","P_NCFTM","P_NCWKD","P_OCTID","PLGSTS","EV_RANGE","UNIT_6","PCHGTM06","SOC_DSP"]
scheduleLlist = ["P_SETSTS","P_TMRAVA","P_ADDDSP","P_EDTDSP","A_SETNXT",
                 "P_SETID","P_SETON","P_SETTYP","P_SETSTM","P_SETFTM","P_SETWKD","P_SETNXT","CLKFMTSW"]
optimumList = ["A_OCOKNG","P_OCRQFL","P_OCTAVA",
               "A_SETNXT","A_SETNX2",
               "P_USOC2A","P_USOC1A","P_USOC0A","LBTYPE_E","P_OCADFL"]
optimumplan1List = ["P_OCTON","P_OCTTYP","P_LMDLMT","P_OCTSTM","P_LMDSTM","P_OCTFTM","P_LMDFTM","P_OCTWKD","P_LMDWKD"]
optimumplan2List = ["P_OCTON2","p_OCTTY2","P_LMTNO2","P_LMDLM2","P_OCTST2","P_LMDST2","P_OCTFT2","P_LMDFT2","P_OCTWK2","P_LMDWK2"]
currentLimit = ["P_CURAVA","P_CUR200","P_CURSL1","P_CURSL2","P_CURSL3","P_CURSL4","P_LMTAVA","P_LMTNOW","P_LMTSEL"]
powerList = ["P_DPWAVA","P_DPW","P_DPWSL0","P_DPWSL1","P_DPWSL2","P_DPWSL3","P_DPWSL4","P_DPWSL5","P_DPWSL6","P_DPWSL7","P_DPWSL8","P_DPWSL9"]
otherSetting = ["P_SLMAVA","P_SLMNOW","P_SLMSL1","P_SLMSL2","P_SLMSL3","P_SLMSL4","P_SLMSL5","PTSYS","BCOOLSW","TBW_EN","BHEATSW"]
supplySetting = ["P_SPLAVA","P_LMDAVA","P_LMDNW","P_SPLNSO","P_SPLDSP","P_SPLEVW","P_SPLACA","P_SPLDCA","P_SPLEVA","P_SPLHVA","PWSPLT_B","PWSPLT_G"]
chargeLidList = ["QCL_RQTG","QCL_OPEQ","PCLEQPR","PCLEQPL","RPCL_ORQ","LPCL_ORQ","RPCL_CRQ","LPCL_CRQ","PCLPOSIR","PCLPOSIL","RPCL_OPE","LPCL_OPE"]


funcMap = {
        "charging control" : controlList ,
        "schedule charging" : scheduleLlist, 
        # "optimum charging" : optimumList, 
        # "optimum plans1" : optimumplan1List, 
        "optimum plans2" : optimumplan2List, 
        # "current&limit":currentLimit,
        # "charing power":powerList,
        # "limit&battery":otherSetting,
        "supply setting":supplySetting,
        "charge lid":chargeLidList
    }
setValueMap = {"P_OCTID": "A_OCTID", "PCNOWDSP": "A_NCTYP", 
              "P_SETSTS":"A_SETSTS",
              "P_SETID":"A_SETID","P_SETSTM":"A_SETSTM","P_SETFTM":"A_SETFTM", "P_SETWKD":"A_SETWKD","P_SETTYP":"A_SETTYP","P_SETON":"A_SETON",
               "P_OCTON":"A_SETON","P_OCTTYP":"A_SETTYP","P_OCTSTM":"A_SETSTM","P_OCTFTM":"A_SETFTM","P_OCTWKD":"A_SETWKD",
               "P_OCTON2":"A_SETON2","p_OCTTY2":"A_SETMO2","P_LMTNO2":"A_LMTRE2","P_OCTST2":"A_SETST2","P_OCTFT2":"A_SETFT2","P_OCTWK2":"A_SETRE2",
               "P_CURAVA":"A_CURREQ","P_LMTNOW":"A_LMTREQ","P_DPW":"A_DPWREQ","P_SLMNOW" : "A_SLMREQ","BCOOLSW":"L_TBCSW","BHEATSW":"L_TBWSW",
               "P_SPLPOP":"A_SPLMOD","P_LMDNW":"A_SLMDRQ"
              }

#panel
panels = {}
#功能label
settingLabels = {}
#显示值label
resultLabels = {}
resultVars = {}
#设置值edit
editEntities = {}
editVars = {}
#发送结果
buttonItems = {}
#清空结果
buttonResetItems = {}
window = tk.Tk()
log_text = tk.Text(window)
info_text = tk.Text(window)
scrollarbar = tk.Scrollbar(window)

def pandasRead():
    global df
    df = pd.read_excel(io=path, sheet_name=sh, engine='openpyxl')

def xlwingsRead():
    global wb,ws
    wb = xw.Book(path)
    ws = wb.sheets[sh]

def readExcel(sheet):
    #默认使用xlrd库，但是不支持读取xlsx
    #指定使用openpyxl库
    pandasRead()
    xlwingsRead()

def readRows(value):
    rows = df[df.apply(lambda row: row.astype(str).str.contains(str(value)).any(), axis=1)]
    return rows

def readValue(value, line):
    rows = readRows(value)
    if line == "设置值":
        return str(int(rows[line].values[0]))
    return rows[line].values[0]

def setExcel(item,value):
    r = df.loc[df["label"] == item].index[0] + 2
    c = df.columns.get_loc("设置值")+1
    print(f"{item} {r}  {c} {df.iloc[r-2][c-1]}")
    if value == int(df.iloc[r-2][c-1]):
        print("not change")
        return
    xlwingsRead()
    # edit cell
    cell = ws.range(r, c)
    cell.value = value
    wb.save(path)
    wb.app.quit()
    pandasRead()
    #update labels and background
    resultVars[item].set(readValue(item, "result"))
    editVars[item].set(readValue(item, "设置值"))
    if 'red' == resultLabels[item].cget('bg') and "wrong" != str(resultVars[item].get()):
        print('update to default')
        resultLabels[item].config(bg='SystemButtonFace')
    elif "wrong" == str(resultVars[item].get()):
        print('update to red')
        resultLabels[item].config(bg="red")

def read_output(process):
    while True:
        output = process.stdout.readline()
        if output:
            str = output.decode('gbk')
            str = str.strip()  # 去除字符串两端的空白字符
            q.put(str + "\n")


def excute_command():
    command = "adb shell \" logcat -s ChargecontrolModel ChargecontrolModelAPIImpl ChargecontrolModelAPI ChargecontrolFC VehicleChargingManager & "
    command += "logcat -s vehiclesettingCOM | grep 'Chargecontrol' & logcat -s UI-VEHICLE-CHARGE & "
    # command += "logcat -s AndroidRuntime & "
    command += "logcat -s VLogicSvc-SOL VLogicMgr-SOL VSettingModel-SOL & "
    command += "logcat -s VLogicSvc-CHARGING VLogicMgr-CHARGING VSettingModel-CHARGING&\""

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    t = threading.Thread(target=read_output, args={process})
    t.daemon = True
    t.start()

    timeout = 1
    start_time = time.time()
    while True:
        while not q.empty():
            start_time = time.time()
        if time.time() - start_time > timeout:
            process.terminate()
            break

def dump_info():
    time.sleep(3)
    command = "adb shell dumpsys activity service com.iauto.vehiclelogicservice/com.iauto.vehiclelogicservice.service.VehicleLogicService Charging"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    read_output(process)

def set_textVar(textShow, isClear = False):
    # with open(logpath, 'a') as f:
    textShow.config(state="normal")
    if isClear:
        textShow.delete('1.0','end')
    while not q.empty():
        str = q.get()
        # f.write(str)
        textShow.insert('end', str)
        textShow.yview('end')
    textShow.config(state='disabled')

def pntlog(content):
    q.put(str(content)+"\n")

def buttonSet(item, type):
    log_text.config(state="normal")
    log_text.delete('1.0','end')
    log_text.config(state="disabled")
    row = readRows(item)
    row = row.dropna(axis=1)
    row = row.iloc[0]
    pntlog("====================================当前设置=================================")
    pntlog(f"功能: {row['功能']}, 设置值：{row['设置值']}, 显示结果：{row['result']}, 信号：{row['msg']}, datalabel:{row['label']}")
    setExcel(item, int(editVars[item].get()))
    row = readRows(item)
    row = row.dropna(axis=1).iloc[0]
    param = readValue(item, type)
    pntlog("=============================================================================\n")
    pntlog("====================================相关设置=================================")
    setRows = df[df['msg'] == row['msg']]
    if str(param) == 'nan':
        pntlog("wrong value, please check all singal value")
        pntlog("return and no set signal.")
        pntlog(',\n'.join(setRows.apply(lambda setRows:f"{setRows['功能']}\t{setRows['label']}:{setRows['设置值']}\t{setRows['result']})",axis=1)))
        set_textVar(log_text)
        return
    if type == 'set':
        pntlog(',\n'.join(setRows.apply(lambda setRows:f"{setRows['功能']}\t{setRows['label']}:{setRows['设置值']}\t{setRows['result']})",axis=1)))
    pntlog("=============================================================================\n")
    command = f"call D:\Project\c++\\testPanel\\test.bat {param}"
    process = subprocess.Popen(command,stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    process.stdin.write(b'\n')
    process.stdin.flush()
    while True:
        line = process.stdout.readline().rstrip()
        if not line:
            break
        pntlog(line.decode('gbk'))
    set_textVar(log_text)
    t = threading.Thread(target=dump_info)
    t.daemon = True
    t.start()

def editClick(item):
    value = str(readValue(item, "信号值"))
    q.put(value)
    set_textVar(info_text, True)

def update_ui():
    set_textVar(log_text)
    window.after(50, update_ui)

def button_export():
    global logpath,filename
    filename = time.strftime('%Y%m%d%H%M%S')+".log"
    logpath = os.path.join(logdir, filename)
    print(logpath)
    with open(logpath, 'a') as f:
        str = log_text.get('1.0', 'end')
        f.write(str)
    pntlog("\n\n\n-----save done-------\n\n\n")


def mianWindow():
    #prepare excel and read DataFrame
    global path,logdir,logpath,filename,sh
    path = "D:\Documents\Project\Rhine\用例-charging.xlsx"
    filename = time.strftime('%Y%m%d%H%M%S')+".log"
    selectFile()
    logpath = os.path.join(logdir, filename)
    print(logpath)
    sh = "测试用例"
    pandasRead()

    #set window
    window.geometry("1000x900")
    style = ttk.Style(window)
    style.configure('lefttab.TNotebook', tabposition='wn')
    notebook = ttk.Notebook(window, style='lefttab.TNotebook')
    # notebook.grid(row=0, column=0)
    notebook.place(relx=0, rely=0, relwidth=0.8, relheight=0.5)
    # log_text.grid(row=1, column=0)
    log_text.place(relx=0, rely=0.5, relwidth=0.98, relheight=0.5)
    log_text.config(state="disabled")
    # info_text.grid(row=0, column=1)
    info_text.place(relx=0.8, rely=0.05, relwidth=0.2, relheight=0.45)
    info_text.config(state="disabled")
    scrollarbar.place(relx=0.98, rely=0.5, relheight=0.5)
    log_text.config(yscrollcommand=scrollarbar.set)
    scrollarbar.config(command=log_text.yview)

    buttonExp = tk.Button(window, command=button_export, text="reset log")
    buttonExp.place(relx=0.8, rely=0, relheight=0.05, relwidth=0.2)

    global q    
    q = queue.Queue()
    t = threading.Thread(target=excute_command)
    t.daemon = True
    t.start()

    # add panels and labels
    for func in panelNameList:
        panel = tk.Frame(notebook)
        print(func)
        if funcMap.get(func) == None:
            continue
        for i,item in enumerate(funcMap[func]):
            rows = readRows(item)
            resultCms = tk.StringVar(value=str(rows["result"].values[0]))
            editCms = tk.StringVar(value=str(int(rows["设置值"].values[0])))
            resultVars[item] = resultCms
            editVars[item] = editCms
            settinglabel = tk.Label(panel, text=str(rows["功能"].values[0]))
            resultlabel = tk.Label(panel, textvariable=resultCms)
            if resultCms.get() == "wrong":
                resultlabel.config(bg='red')
            editEntity = tk.Entry(panel, textvariable=editCms)
            editEntity.bind("<Button-1>", func=lambda event, item=item:editClick(item))
            editEntity.focus_force()
            button = tk.Button(panel, text=item, command=lambda item=item: buttonSet(item, "set"))
            resetButton = tk.Button(panel, text="reset "+item, command=lambda item=item :buttonSet(item, "reset"))
            settingLabels[item] = settinglabel
            resultLabels[item] = resultlabel
            editEntities[item] = editEntity
            buttonItems[item] = button
            buttonResetItems[item] = resetButton
            settinglabel.grid(row=i, column=0, padx=0)
            resultlabel.grid(row=i, column=1, padx=10)
            editEntity.grid(row=i, column=2, padx=10)
            button.grid(row=i, column=3, padx=10)
            resetButton.grid(row=i, column=4, padx=10)
        notebook.add(panel, text=func)
    window.after(50, update_ui)
    window.mainloop()

def selectFile():
    global logdir
    logdir = filedialog.askdirectory()
    print(logdir)

if __name__ == '__main__':
    # df = readExcel("D:\Documents\Project\Rhine\用例-charging.xlsx","测试用例")
    command = f"call D:\Project\c++\\testPanel\log-set.bat "
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    mianWindow()