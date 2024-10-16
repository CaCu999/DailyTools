import tkinter as tk
import subprocess
import queue
from tkinter import filedialog
import time
import threading
import os
import json

window = tk.Tk()
log = tk.Text(window)
logtag = tk.Text(window)
filebox = tk.Listbox(window)
propVar = tk.StringVar()
nameVar = tk.StringVar()
cuspropVar = tk.StringVar()
cusvalueVar = tk.StringVar()

def selectFile():
    path = filedialog.askdirectory()
    return path

def is_adb_connected():
    result = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    # 如果输出中包含 "no devices/emulators found"，则设备被认为是断开连接的
    # print(result.stdout)
    # print(f"size is : {len(result.stdout.splitlines())}")
    interrupt = len(result.stdout.splitlines()) < 3
    # print(f"size is : {len(result.stdout.splitlines())}")
    return interrupt

def adb_clear():
    result = subprocess.run(["adb", "logcat -c"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    log.config(state="normal")
    log.delete('1.0','end')
    log.config(state="disabled")
    logpnt("---clear all---\n\n\n")

def read_output(process):
    global interrupt,stop
    while True:
        # if process.poll() is not None:
        #     break
        if stop:
            logpnt("interrupt...")
            process.terminate()
            if is_adb_connected():
                set_textVar(log, True)
                logpnt("adb connection lost. restarting command...")
                logpnt("interrupt...")
                process.terminate()
                break
            break
        output = process.stdout.readline()
        if output:
            # str = output.decode('gbk')
            try:
                str = output.decode()
            except:
                continue
            str = str.strip()  # 去除字符串两端的空白字符
            q.put(str + "\n")
            start = time.time()
    log_set()
    # if stop or is_adb_connected():
    adb_clear()
    process.terminate()
    stop = False
    excute_command()


def dump_info(value):
    ori = "adb shell dumpsys activity service com.iauto.vehiclelogicservice/com.iauto.vehiclelogicservice.service.VehicleLogicService"
    command = ori
    if len(value.split(" "))  == 2:
        ls = value.split(" ")
        if props[ls[0]] is not None:
            ls[0] = props[ls[0]]
            value = "prop" + " " + ls[0] + " " + ls[1]
    if value != "":
        command = f"{command} {value}"
    else:
        command = f"{command}"
    q.put(command+"\n")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # read_output(process)
    global interrupt,stop
    while True:
        if process.poll() is not None:
            break
        if stop:
            logpnt("interrupt...") 
            if is_adb_connected():
                set_textVar(log, True)
                logpnt("adb connection lost. restarting command...")
                logpnt("interrupt...")
                process.terminate()
                break
            process.terminate()
            break
        output = process.stdout.readline()
        if output:
            # str = output.decode('gbk')
            str = output.decode()
            str = str.strip()  # 去除字符串两端的空白字符
            q.put(str + "\n")
        else:
            break


def log_set():
    command = "call " + os.path.join(os.path.dirname(__file__), "file","log-set.bat")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def prop_set(prop):
    command = "adb shell setprop persist.log.tag."+prop +" V"
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    # print(command)

def excute_command():
    tags = logtag.get('2.0','end').split('\n')
    command = "adb shell \"  "
    # for tag in tags:
    #     if tag.__contains__("|") : tag = tag.split('|')[0]
    #     if tag.startswith("#") or len(tag) == 0: continue
    #     prop_set(tag)
    for tag in tags:
        if tag.startswith("#") or tag == "":
            continue
        command += f"logcat -s {tag} & "
    command += "\""
    command += "\n"
    logpnt(command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    read_output(process)

def button_set():
    prop = propVar.get()
    t = threading.Thread(target=dump_info, args=(prop,), name="dumpinfo")
    t.daemon = True
    t.start()
    set_textVar(log, False)

def update_ui():
    set_textVar(log)
    window.after(100, update_ui)

def button_reset():
    log.config(state="normal")
    log.delete('1.0','end')
    log.config(state="disabled")
    update_logpath()

def button_ensure_key():
    # adb_clear()
    global stop
    stop = True
    lines = logtag.get('2.0','end').split("\n")
    config_logtag(lines)
    t = threading.Thread(target=excute_command, name="excute_command")
    t.daemon = True
    t.start()
    set_textVar(log, False)
    with open(logtagpath, 'w') as f:
        str = logtag.get('2.0', 'end')
        f.write(str) 

def set_textVar(textShow, isClear = False):
    # with open(logpath, 'a') as f:
    key = cuspropVar.get()
    textShow.config(state="normal")
    if isClear:
        textShow.delete('1.0','end')
    while not q.empty():
        str = q.get()
        if key in str:
            start = str.find(key)
            end = start + len(key)
            textShow.insert('end', str[:start])                      # 插入key前的文本
            textShow.insert('end', str[start:end], "highlight")      # 插入key，并添加tag
            textShow.insert('end', str[end:])                        # 插入key后的文本
        else:
            textShow.insert('end', str)
        # textShow.insert('end', str)
        textShow.yview('end')
    textShow.config(state='disabled')

def logpnt(str):
    q.put(str + "\n")

def update_logpath():
    global logpath,filename
    name = nameVar.get()
    if name == "" :
        # print(time.strftime('%Y%m%d%H%M%S')+".log")
        filename = time.strftime('%Y%m%d%H%M%S')+".log"
    else:
        # print(name)
        filename = name + '_' + time.strftime('%d%H%M%S')+".log"
    logpath = os.path.join(logdir, filename)

def export_log():
    update_logpath()
    with open(logpath, 'a') as f:
        str = log.get('1.0', 'end')
        f.write(str)
    logpnt("\n\n\n-----save done-------\n\n\n")
    global file_paths
    while len(file_paths) > 3:
        file_paths.pop()
        filebox.delete(0)
    filebox.insert(len(file_paths), logpath)
    file_paths.append(logpath)

def config_logtag(lines):
    logtag.config(state="normal")
    logtag.tag_remove("highlight", '1.0', 'end')  # 删除之前的 "highlight" 标签
    logtag.delete('1.0','end')
    logtag.insert('end', "\t去除此tag请以#开头或直接删除\n")
    for index, line in enumerate(lines, start=2):
        line = line.replace("\n","")
        if line != "":
            logtag.insert('end', line + "\n")
        if not line.startswith("#") and line != '':
            start = f'{index}.0'
            end = f'{index}.end'
            logtag.tag_add("highlight", start, end)
    logtag.yview('end')
    
def open_file(filedir):
    os.startfile(filedir)

def open_dir():
    os.startfile(logdir)

def main_window():
    global q,logpath,logdir,logtagpath,stop
    global file_paths
    global props
    proppath = os.path.join(os.path.dirname(__file__), "file" , "propList.json")
    with open(proppath) as file:
        props = json.load(file)
    file_paths = []
    q = queue.Queue()
    stop = False
    filename = time.strftime('%Y%m%d%H%M%S')+".log"
    logdir = selectFile()
    if logdir == "":
        return
    logpath = os.path.join(logdir, filename)
    # logtagpath = os.path.join(logdir, "logtag.txt")
    logtagpath = "testPanel\log-filter.txt"
    logtagpath = os.path.join(os.path.dirname(__file__), "file" , "log-filter.txt")
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
    labelName = tk.Label(window, text="filename")
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

    #file path
    # label_path = tk.Label(window, text="filedir")
    # label_path.place(relheight=0.05, relwidth=0.1, relx=0.01, rely=0.18)
    filebox.place(relheight=0.1, relwidth=0.27, relx=0.01, rely=0.18)
    filebox.bind('<Double-Button-1>', lambda event: open_file(filebox.get(filebox.curselection())))    
    # button of set ensure_key value
    dirButton = tk.Button(window, text="open dir", command=open_dir)
    dirButton.place(relheight=0.045, relwidth=0.1, relx=0.29, rely=0.18)

    exportButton = tk.Button(window, text="export", command=export_log)
    exportButton.place(relheight=0.05, relwidth=0.1, relx=0.29, rely=0.23)
    
    # log panel
    log.place(relwidth=0.98, relheight=0.68, relx=0, rely=0.32)
    log.config(state="disabled")
    log.tag_config("highlight", background='yellow')   
    scrolllog = tk.Scrollbar(window)
    scrolllog.place(relwidth=0.02, relheight=0.68, relx=0.98, rely=0.32)
    log.config(yscrollcommand=scrolllog.set)
    scrolllog.config(command=log.yview)

    global interrupt
    interrupt = False
    t = threading.Thread(target=excute_command, name = "excute_command-1")
    t.daemon = True
    t.start()
    # p = threading.Thread(target=is_adb_connected)
    # p.daemon = True
    # p.start()
    window.after(100, update_ui)
    window.mainloop()

if __name__ == "__main__":
    log_set()
    main_window()