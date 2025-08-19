from tkinter import filedialog
import pandas as pd
import os
import json
import subprocess

def read_trans_file(file: str):
    if file == "":
        return
    sh = os.path.basename(file)
    # print(file)
    # print(sh)
    sympath = os.path.join(os.path.dirname(__file__), "file" , "logSymbol.json")
    with open(sympath) as f:
        data = json.load(f)
    print(data)
    proppath = os.path.join(os.path.dirname(__file__), "file" , "propSymbol.json")
    with open(proppath) as f:
        prop = json.load(f)
    df = pd.read_csv(file)
    select_rows = df[df['LOG_TYPE'] == "EVENT LOG"]
    print(select_rows)
    path = os.path.dirname(file)
    path = os.path.join(path, sh.split(".")[0] + ".log")
    print(path)
    print(df.columns)
    with open(path, 'a') as f:
        for index,row in select_rows.iterrows():
            lapse = "{:.3f}".format(row['TICKCOUNT(ms)']/1000)
            time = row['DATE_TIME'] 
            log_data = str(row['LOG_DATA'])
            if len(log_data.split("|")) == 0:
                continue
            eventID = log_data.split("|")[0].replace("EventID:", "")
            func = data[log_data.split("|")[0]] if data.get(log_data.split("|")[0]) is not None else log_data.split("|")[0]
            print(log_data)
            print(len(log_data.split("|")))
            if len(log_data.split("|")) != 1:
                content = log_data.split("|")[1]
                content = content.replace("DynamicData:","")
                content = prop[content] if prop.get(content) is not None else prop[content.upper()] if prop.get(content.upper()) is not None else content
                line = f"{lapse} {time} {eventID} {func}: {content}\n"
            else:
                line = f"{lapse} {time} {eventID} {func}\n"
            f.write(line)
            print(line)

def mainWindow():
    exefile = os.path.join(os.path.dirname(__file__), "file" , "TraceFileParser_200710.exe")
    # exefile = "D:\\Software\\DTLOG解密解析工具\\TraceFileParser_200710.exe"
    result = subprocess.run(exefile, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    # file = filedialog.askopenfilename(filetypes= [("all files", "*.csv")])
    files = filedialog.askopenfilenames(filetypes=[("all files", "*.csv")])
    for file in files:
        read_trans_file(file)
        

if __name__ == "__main__":
    mainWindow()