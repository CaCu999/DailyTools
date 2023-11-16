import tkinter as tk
import subprocess
import queue
from tkinter import filedialog
import time
import threading
import os

window = tk.Tk()
log = tk.Text(window)
logtag = tk.Text(window)
propVar = tk.StringVar()
nameVar = tk.StringVar()
cuspropVar = tk.StringVar()
cusvalueVar = tk.StringVar()

def selectFile():
    path = filedialog.askdirectory()
    if path=="":
        path = os.path.expanduser('~')
        path = os.path.join(path, 'Desktop')
    return path

def is_adb_connected():
    global interrupt
    while True:
        startT = time.time()
        result = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        # 如果输出中包含 "no devices/emulators found"，则设备被认为是断开连接的
        # print(result.stdout)
        print(f"size is : {len(result.stdout.splitlines())}")
        interrupt = len(result.stdout.splitlines()) < 3

def adb_clear():
    result = subprocess.run(["adb", "logcat -c"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    log.config(state="normal")
    log.delete('1.0','end')
    log.config(state="disabled")
    logpnt("---clear all---\n\n\n")

def read_output(process):
    global interrupt
    timeout = 10
    start = time.time()
    while not interrupt and not stop:
        if time.time() - start > timeout:
            print(f"{time.time() - start}")
            start = time.time()
            if interrupt:
                logpnt("adb connection lost. restarting command...")
                process.terminate()
                break
        output = process.stdout.readline()
        # print(output)
        if output:
            # str = output.decode('gbk')
            str = output.decode()
            str = str.strip()  # 去除字符串两端的空白字符
            q.put(str + "\n")
            start = time.time()
    while interrupt:
        if time.time() - start > timeout:
            print(f"wait ... {time.time() - start}")
            break
    log_set()
    adb_clear()
    if stop:
        excute_command()  # 重新执行命令    

def dump_info(value, custum = False):
    print(value)
    ori = "adb shell dumpsys activity service com.iauto.vehiclelogicservice/com.iauto.vehiclelogicservice.service.VehicleLogicService"
    command = ori
    if custum:
        command = f"{command} {value}"
    else:
        command = f"{command} Charging"
    q.put(command+"\n")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    read_output(process)
    time.sleep(3)
    command = ori
    print(command)
    q.put(command)
    process2 = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    read_output(process2)

def log_set():    
    command = f"call D:\Project\c++\\testPanel\log-set.bat "
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def excute_command():
    tags = logtag.get('2.0','end').split('\n')
    print(tags)
    command = "adb shell \"  "
    for tag in tags:
        if tag.startswith("#") or tag == "":
            continue
        command += f"logcat -s {tag} & "
    command += "\""
    command += "\n"
    # command += "adb shell \"  "
    # # command += "logcat -s vehiclesettingCOM | grep 'Chargecontrol' & "
    # # command += "logcat -s UI-VEHICLE-CHARGE & "
    # # command += "logcat -s SystemUICOM & "
    # # command += "logcat -s UI-SYSTEMUI-COM & "
    # # command += "logcat -s UI-VEHICLE-VEHICLEEXTERIOR  vehiclesettingCOM & "
    # command += "logcat -s libvehiclecharging & "
    # command += "logcat -s libvehiclesolarcharging & "
    # # command += "logcat -s AndroidRuntime & "
    # command += "logcat -s VLogicSvc-SOL VLogicMgr-SOL VSettingModel-SOL & "
    # command += "logcat -s VLogicSvc-CHARGING VLogicMgr-CHARGING VSettingModel-CHARGING& \""

    # command = f"call  \"D:\Project\c++\\testPanel\log-filter.bat\" "
    logpnt(command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    read_output(process)

def button_set():
    prop = propVar.get()
    t = threading.Thread(target=dump_info, args=(prop, False))
    t.daemon = True
    t.start()
    # logtag.config(state="normal")
    # with open(logtagpath,"a") as f:
    #     logtag.insert('end', prop + "\t" + value + "\n")
    #     f.write(prop + "\t" + value + "\n")
    # logtag.yview('end')
    # logtag.config(state="disabled")
    # global logpath
    # logpath = os.path.join(logdir, f"{prop.upper()}_{time.strftime('%H%M%S')}.log")
    set_textVar(log, False)

def update_ui():
    set_textVar(log)
    window.after(50, update_ui)

def button_reset():
    log.config(state="normal")
    log.delete('1.0','end')
    log.config(state="disabled")
    global logpath,filename
    name = nameVar.get()
    if name == "" :
        print(time.strftime('%Y%m%d%H%M%S')+".log")
        filename = time.strftime('%Y%m%d%H%M%S')+".log"
    else:
        print(name)
        filename = name + '_' + time.strftime('%d%H%M%S')+".log"
    logpath = os.path.join(logdir, filename)
    print(logpath)

def button_ensure_key():
    prop = cuspropVar.get()
    # value = cusvalueVar.get()
    # t = threading.Thread(target=dump_info, args=(prop, True))
    # t.daemon = True
    # t.start()
    lines = logtag.get('2.0','end')
    config_logtag(lines)
    global stop
    stop = True
    t = threading.Thread(target=excute_command)
    t.daemon = True
    t.start()
    # logtag.config(state="normal")
    # with open(logtagpath,"a") as f:
    #     logtag.insert('end', prop + "\t" + value + "\n")
    # f.write(prop + "\t" + value + "\n")
    # logtag.yview('end')
    # logtag.config(state="disabled")
    # global logpath
    # logpath = os.path.join(logdir, f"{prop.upper()}_{value}_{time.strftime('%Y%m%d%H%M%S')}.log")
    set_textVar(log, True)
    with open(logtagpath, 'w') as f:
        str = logtag.get('2.0', 'end')
        f.write(str)

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

def logpnt(str):
    q.put(str + "\n")

def export_log():
    with open(logpath, 'a') as f:
        str = log.get('1.0', 'end')
        f.write(str)
    logpnt("\n\n\n-----save done-------\n\n\n")

def config_logtag(lines):
    print("config_logtag______")
    logtag.config(state="normal")
    logtag.tag_remove("highlight", '1.0', 'end')  # 删除之前的 "highlight" 标签
    logtag.delete('1.0','end')
    logtag.insert('end', "\t去除此tag请以#开头或直接删除\n")
    for index, line in enumerate(lines, start=2):
        if line != "":
            logtag.insert('end', line)
        if not line.startswith("#") and line != '':
            start = f'{index}.0'
            end = f'{index}.end'
            logtag.tag_add("highlight", start, end)           
    logtag.yview('end')
    
def main_window():
    global q,logpath,logdir,logtagpath,stop
    q = queue.Queue()
    stop = False
    filename = time.strftime('%Y%m%d%H%M%S')+".log"
    logdir = selectFile()
    logpath = os.path.join(logdir, filename)
    logtagpath = os.path.join(logdir, "logtag.txt")
    window.geometry("1000x800")    
    # logtag panel
    logtag.place(relwidth=0.73, relheight=0.3, relx=0.4, rely=0)
    logtag.tag_config("highlight", background='yellow')
    logtag.config(state="disabled")
    scrollloghis = tk.Scrollbar(window)
    scrollloghis.place(relwidth=0.02, relheight=0.3, relx=0.98, rely=0.0)
    logtag.config(yscrollcommand=scrollloghis.set)
    scrollloghis.config(command=logtag.yview)

    # property
    labelProp = tk.Label(window, text="dumpKey")
    labelProp.place(relheight=0.05, relwidth=0.1, relx=0.01, rely=0)
    entityProp = tk.Entry(window, textvariable=propVar)
    entityProp.place(relheight=0.05, relwidth=0.15, relx=0.11, rely=0)
    entityProp.focus_force()   
    button = tk.Button(window, text="dump", command=button_set)
    button.place(relheight=0.05, relwidth=0.07, relx=0.27, rely=0)

    # filename
    labelName = tk.Label(window, text="value ")
    labelName.place(relheight=0.05, relwidth=0.1, relx=0.01, rely=0.06)
    entityName = tk.Entry(window, textvariable=nameVar)
    entityName.place(relheight=0.05, relwidth=0.15, relx=0.11, rely=0.06)
    entityName.focus_force()
    resetButton = tk.Button(window, text="reset", command=button_reset)
    resetButton.place(relheight=0.05, relwidth=0.07, relx=0.27, rely=0.06)

    # ensure logtag setting
    label_ensurekey = tk.Label(window, text="filter-tag")
    label_ensurekey.place(relheight=0.05, relwidth=0.1, relx=0.01, rely=0.12)
    entity_ensurekey = tk.Entry(window, textvariable=cuspropVar)
    entity_ensurekey.place(relheight=0.05, relwidth=0.15, relx=0.11, rely=0.12)
    entity_ensurekey.focus_force()
    ensurekeyButton = tk.Button(window, text="ensure_key", command=button_ensure_key)
    ensurekeyButton.place(relheight=0.05, relwidth=0.07, relx=0.27, rely=0.12)

    with open(logtagpath, "a") as f:
        pass
    with open(logtagpath, "r") as f:
        lines = f.readlines()
        config_logtag(lines)

    entityensure_keyVal = tk.Entry(window, textvariable=cusvalueVar)
    entityensure_keyVal.place(relheight=0.05, relwidth=0.2, relx=0.14, rely=0.2)
    entityensure_keyVal.focus_force()

    # button of set ensure_key value
    exportButton = tk.Button(window, text="export", command=export_log)
    exportButton.place(relheight=0.05, relwidth=0.1, relx=0.15, rely=0.26)
    # log panel
    log.place(relwidth=0.98, relheight=0.68, relx=0, rely=0.32)
    log.config(state="disabled")
    scrolllog = tk.Scrollbar(window)
    scrolllog.place(relwidth=0.02, relheight=0.68, relx=0.98, rely=0.32)
    log.config(yscrollcommand=scrolllog.set)
    scrolllog.config(command=log.yview)

    global interrupt
    interrupt = False
    t = threading.Thread(target=excute_command)
    t.daemon = True
    t.start()
    p = threading.Thread(target=is_adb_connected)
    p.daemon = True
    p.start()
    window.after(50, update_ui)
    window.mainloop()

if __name__ == "__main__":
    log_set()
    main_window()