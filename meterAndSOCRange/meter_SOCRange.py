import tkinter as tk
from canlib.kvadblib import dbc
from canlib import kvadblib
import os
import json
from canlib.kvadblib import message
import math
from canlib import Frame

#define
def global_define():
    dbcPath = os.path.join(os.path.dirname(__file__), "file","CAN2M.dbc")
    global dbcFile,CANMap,SOCMap,historyMap,hisfile
    try:
        dbcFile = dbc.Dbc(dbcPath)
    except kvadblib.KvdDbFileParse:
        print(kvadblib.get_last_parse_error())
    file = os.path.join(os.path.dirname(__file__), "file","Meter.json")
    with open(file) as f:
        CANMap = json.load(f)
    file = os.path.join(os.path.dirname(__file__), "file", "SOC.json")
    with open(file, encoding="utf-8") as f:
        SOCMap = json.load(f)
    historyMap = {}
    hisfile = os.path.join(os.path.dirname(__file__), "file", "history.json")
    with open(hisfile) as f:
        historyMap = json.load(f)
   
def getMsg(msgName:str):
    mm = dbcFile.get_message_by_name(msgName)
    msg = mm.bind()
    return msg

def writeSignalValue(msg:message.BoundMessage, signalName:str, value:int):
    att = getattr(msg, signalName)
    setattr(att, "phys", value)
    # print(msg._data)
    # print(msg._frame)
    return msg

def transStr2Int(input:str):
    res = 0
    input = input.strip()
    if not input:
        return 0
    elif input.endswith('b') or input.endswith('B'):
        res = int(input[:-1], 2)
    elif input.endswith("h") or input.endswith('H'):
        res = int(input[:-1], 16)
    else:
        res = int(input)
    return res

def save2Json():
    global historyMap
    json_string = json.dumps(historyMap)
    # print(json_string)
    with open(hisfile, "w") as f:
        f.write(json_string)

class Application(tk.Tk):
    def logpnt(self, log):
        log = str(log)
        self.__log.config(state="normal")
        self.__log.insert('end', log + "\n")
        self.__log.config(state="disabled")
        self.__log.yview('end')
    
    # 说明：
    # 03 73 56 ：固定，表示can报文
    # 0E ：后面数据长度
    # 00 ：占位，无具体含义
    # 53 F7 ：5 CAN类型（0:Global CAN G5M，5:Local CAN 5，C:Global CAN G2M_1），3 F7 canId
    # 00 ：分组Id，固定0即可
    # 09 ：后面数据长度
    # 01 ：途绝状态
    # 35 ~ 最后：CAN报文数据
    def button_ensure(self, msg:str, timeout:bool):
        self.logpnt(f"timeout {timeout}")

        m_message = getMsg(msg)
        self.logpnt(m_message._frame)
        # arrys = bytearray()
        # id = m_message._frame.id.to_bytes()
        for signal in CANMap[msg]:
            res = self.getFromVar(signal)
            self.logpnt(f"{msg}.{signal}: {self.__signals[signal].get()} -> {res}")
            m_message = writeSignalValue(m_message, signal, res)
            self.logpnt(m_message._data)
            # self.__signals[signal].set(self.)
        save2Json()
        

    def getFromVar(self, signal):
        res = self.__signals[signal].get()
        global historyMap
        historyMap[signal] = res
        self.logpnt(f"{signal}:{res} -> {transStr2Int(res)}")
        return transStr2Int(res)

    def updateText(self, oriStr:list, resStr:list):
        for i,item in enumerate(SOCMap):
            self.logpnt(f"\n==={item}===")
            sig_str = str()
            for signal in SOCMap[item]:
                sig_str += f"{signal}:\t{historyMap[signal]}\t\t"
            self.logpnt(sig_str)
            self.logpnt(f"{i} {item[1:-1]}: {resStr[i]}")
            self.__text[item][0].set(oriStr[i])
            self.__text[item][1].set(resStr[i])
    
    def button_caculate(self):
        cngpievd = self.getFromVar("CNGPIEVD")
        pievd100 = self.getFromVar("PIEVD100")
        pievdsr = self.getFromVar("PIEVDSR")
        range = 0
        oriStr = []
        resStr = []
        str1 = str()
        str2 = str()
        if cngpievd == 0:
            range = pievd100 / 10
            str1 = f"(航続距離)=(PIEVD100)"
            str2 = f"{range} = {pievd100}"
        elif cngpievd == 1:
            range = pievd100 / 10 * (100 - pievdsr) / 100
            str1 = f"(航続距離)=(PIEVD100)*(100-PIEVDSR)/100"
            str2 = f"{range} = {pievd100} * (100- {pievdsr} )/100"
        else:
            str1 = f"no ptsys, not display"
            str2 = f"not display"
        oriStr.append(str1)
        resStr.append(str2)
        unit_6 = self.getFromVar("UNIT_6")
        if unit_6 == 1 or unit_6 == 2:
            str1 = f"(航続距離)=(減算率処理後の航続距離)"
            str2 = f"{range} = {range}"
        elif unit_6 == 3 or unit_6 == 4:
            range = range / 1.609
            str1 = f"(航続距離)=(減算率処理後の航続距離) / 1.609"
            str2 = f"{range} = {range} / 1.609 = {range}"
        else:
            str1 = f"no ptsys, not display"
            str2 = f"not display"
        range = math.ceil(range)
        str2 += f" -> {range}"
        oriStr.append(str1)
        resStr.append(str2)
        ptsys = self.getFromVar("PTSYS")
        limit = self.getFromVar("P_LMTNOW")
        limit = (10 - limit) * 10
        evrange = self.getFromVar("EV_RANGE")
        pieve06 = self.getFromVar("PIEVE06")
        socdsp = self.getFromVar("SOC_DSP")
        div = 25
        if ptsys == 5:
            # str1 = f"(予想走行可能距離)=(単位変換処理の航続距離) / 100 * (P_LMTNOW - SOC_DSP) + EV_RANGE"
            # str2 = f"{range}={range} / 100 * ({limit} - {socdsp}) + {evrange}"
            str1 = f"(予想走行可能距離)=(単位変換処理の航続距離) / 25 * (P_LMTNOW - SOC_DSP) + EV_RANGE"
            str2 = f"{range}={range} / {div} * ({limit} - {socdsp}) + {evrange}"
            range = range / div * (limit - socdsp) + evrange
            str2 += f" = {range}"
        elif ptsys == 4:
            # str1 = f"(予想走行可能距離)=(単位変換処理の航続距離) / 100 * (P_LMTNOW - PIEVE06) + EV_RANGE"
            # str2 = f"{range}={range} / 100 * ({limit} - {pieve06}) + {evrange}"
            str1 = f"(予想走行可能距離)=(単位変換処理の航続距離) / 25 * (P_LMTNOW - PIEVE06) + EV_RANGE"
            str2 = f"{range}={range} / {div} * ({limit} - {pieve06}) + {evrange}"
            range = range / div * (limit - pieve06) + evrange
            str2 += f" = {range}"
        else:
            str1 = f"no ptsys, not display"
            str2 = f"not display"
        range = math.ceil(range)
        str2 += f" -> {range}"
        oriStr.append(str1)
        resStr.append(str2)
        self.updateText(oriStr, resStr)
        save2Json()


    def getItemFromMap(self, part1:tk.Frame, map:map, type:int):
        for key in map:
            #create message panel
            panel = tk.Frame(part1,
                            highlightbackground="black",  # 设置边框颜色
                            highlightthickness=1,        # 设置边框粗细
                            height=20)
            panel.pack(side=tk.TOP, anchor="nw", fill=tk.X, expand=True)
            #message name
            label = tk.Label(panel, bg="lightgray", text=key)
            label.pack(side=tk.LEFT)

            j = 0
            for signal in map[key]:
                if j%8 == 0:
                    #create signal panel
                    panel_signal = tk.Frame(part1)
                    panel_signal.pack(side=tk.TOP, anchor="nw", fill=tk.X, pady=5)
                #add signals
                label = tk.Label(panel_signal, text=signal)
                if self.__signals.get(signal) is None:
                    variable = tk.StringVar()
                    self.__signals[signal] = variable
                else:
                    variable = self.__signals[signal]
                entry = tk.Entry(panel_signal, textvariable=variable)
                label.pack(side=tk.LEFT, fill=tk.X)
                entry.pack(side=tk.LEFT, fill=tk.X)
                # label.grid(row = int(j/6), column=j%6)
                # entry.grid(row= int(j/6), column=(j+1)%6)
                if historyMap.get(signal) is None:
                    historyMap[signal] = variable.get()
                variable.set(historyMap[signal])
                j+=2
            if type == 1: #Can simulate
                #create signal panel
                # panel_button = tk.Frame(part1)
                # panel_button.pack(side=tk.TOP, anchor="nw", fill=tk.X, pady=5)
                button = tk.Button(panel_signal, text="ensure", command=lambda k=key, timeout = False, s=signal: self.button_ensure(k, timeout))
                button2 = tk.Button(panel_signal, text="timeout", command=lambda k=key, timeout = True, s=signal: self.button_ensure(k, timeout))
                button.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
                button2.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
                # button.grid(row = int(j/6) + 1, column=2)
                # button2.grid(row = int(j/6) + 1, column=3)
            elif type == 2:
                text_panel = tk.Frame(part1)
                text_panel.pack(side=tk.TOP, anchor="nw", fill=tk.X, pady=5)
                textVar = tk.StringVar()
                text = tk.Entry(text_panel, textvariable=textVar)
                text.config(state="disabled")
                text.pack(side=tk.TOP, anchor="nw", fill=tk.X, expand=True)
                self.__text[key] = []
                self.__text[key].append(textVar)
                # print(f"---> {self.__text}")

                textVar = tk.StringVar()
                text = tk.Entry(text_panel, textvariable=textVar)
                text.config(state="disabled")
                text.pack(side=tk.TOP, anchor="nw", fill=tk.X, expand=True)
                self.__text[key].append(textVar)
        if type == 2:
            # panel_button = tk.Frame(part1)
            # panel_button.pack(side=tk.TOP, anchor="nw", fill=tk.X, pady=5)
            button = tk.Button(panel_signal, text="caculate", command=self.button_caculate)
            button.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
            


    def __init__(self):
        super().__init__()
        self.__signals = {}
        self.__text = {}
        self.geometry("900x700")
        part1 = tk.Frame(self)
        part2 = tk.Frame(self)
        part1.place(relx=0, rely=0,relwidth=1, relheight=0.75)
        part2.place(relx=0, rely=0.75,relwidth=1, relheight=0.25)
        self.getItemFromMap(part1, CANMap, 1)
        self.getItemFromMap(part1, SOCMap, 2)
        self.__log = tk.Text(part2)
        self.__log.config(state="disabled")
        # self.__log.pack(side=tk.LEFT, anchor="nw", fill=tk.X, expand=True)
        self.__log.place(relx=0, rely=0, relwidth=0.975, relheight=1)
        scroll = tk.Scrollbar(part2)
        self.__log.config(yscrollcommand=scroll.set)
        # scroll.pack(side=tk.LEFT, anchor="nw", fill=tk.X, expand=True)
        scroll.place(relx=0.975, rely=0, relwidth=0.02, relheight=1)



if __name__ == "__main__":
    global_define()
    app = Application()
    app.mainloop()