import tkinter as tk
from tkinter import ttk
import subprocess
import os
import openpyxl.worksheet
import openpyxl.worksheet.worksheet
from svn.common import CommonClient
import urllib.parse
from tkinter import filedialog
import shutil
import time
import openpyxl
from openpyxl import load_workbook
import threading
import queue

varlist = {
    'date': time.strftime('%Y/%m/%d'),
    'tickid':'',
    'vehicletype':'Lexus',
    'socversion':'',
    'mcuversion':'',
    'compress':''
}
varIndex = {
    'date':{},
    'tickid': {'汇总':'D3'},
    'vehicletype': {'汇总':'D4'},
    'socversion': {'汇总':'D8'},
    'mcuversion': {'汇总':'D9'},
    'compress': {'汇总':'D10'}
}
# 1. 确认所有需要对应的模块
def getlist():
    mode_list = []
    for i in range(1, 27):
        mode_list.append(f'2.11.{i}')
    # print(mode_list)
    return mode_list

def run_command(cmd):
    result = subprocess.run(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding='gbk')
    return result.stdout

def updatedir(path):
    path = 'D:/WorkProject/Mecna/01_开发库/22_Release/WeeklyRelease/开发ReleaseCheck/'
    res1 = run_command(['svn', 'info', path])
    print(res1)
    res2 = run_command(['svn', 'update', path])
    print(res2)  

def replaceCellValue(sheet:openpyxl.worksheet.worksheet, loc:str, val:str):
    cell = sheet[loc]
    cell.value = val
    

class Application(tk.Tk):
    def cmd_btn_ensure(self):
        path = filedialog.askdirectory()
        self.__var.set(path)
        updatedir(path)

# 2. 在上一个路径里面找到文件
    def getfile(self):
        if self.__menu.get() == "":
            self.log_pnt("no model id selected.")
            return
        id = self.__menu.get() + '_'
        self.log_pnt(id)
        path = self.__var.get()
        self.log_pnt(path)
        dirs = os.listdir(path)
        dirs.sort(key=lambda x: os.path.getctime(os.path.join(path, x)), reverse=True)
        last = os.path.join(path, dirs[1])
        files = os.listdir(last)
        self.log_pnt(files)
        filename = ""
        for (index, item) in enumerate(files):
            if item.__contains__(id):
                self.log_pnt(f'{item}:  {item.__contains__(id )}')
                filename = item
                break
        self.log_pnt("get result of dirs")
        if filename == "":
            self.log_pnt('not found filename')
            return
        new = os.path.join(path, dirs[0])
        # self.log_pnt(filename)
        if not os.path.exists(os.path.join(new, filename)):
# 3. 移动文件到新路径
            shutil.copy(os.path.join(last, filename), new)
            self.log_pnt('====copy end=====')
            self.log_pnt(f'filename:{filename}')
            self.log_pnt(os.listdir(new))
        else:
            self.log_pnt('====contains=====')
            self.log_pnt(f'filename:{filename}')
            self.log_pnt(f'dir:{new}')
        self.__path = os.path.join(new, filename)
        self.log_pnt(f"outpath: {self.__path}")


    # 4. 打开新路径的文件，填入信息
    def writ_newfile(self):
        self.ensure_import()
        self.getfile()
        self.log_pnt('get file ent.........')
        path = self.__path
        book = openpyxl.load_workbook(path)
        self.log_pnt(f"book['变更履历'], 'C4', {varlist['date']}")
        replaceCellValue(book['变更履历'], 'C4', varlist["date"])
        self.log_pnt(f"book['变更履历'], 'H4', Release Check({varlist['tickid']})")
        replaceCellValue(book['变更履历'], 'H4', f'Release Check({varlist["tickid"]})')
        self.log_pnt(f"book['变更履历'], 'J4', [Vehicle]WeeklyRelease {varlist['date']}_ReleaseCheck")
        replaceCellValue(book['变更履历'], 'J4', f'[Vehicle]WeeklyRelease {varlist["date"]}_ReleaseCheck')
        for (i, item) in enumerate(varlist):
            for (j, index) in enumerate(varIndex[item]):
                self.log_pnt(f"book[{index}], {varIndex[item][index]}, {varlist[item]}")
                replaceCellValue(book[index], varIndex[item][index], varlist[item])
        sh = book['测试明细']
        for (i, cell) in enumerate(sh['S']):
            if i < 4:
                continue
            version = varlist['compress'] if varlist['compress'] != "" else varlist['socversion']
            version = '-' if version == "" else version
            self.log_pnt(f'{i}:  {cell.value} {version}')
            cell.value = version
        for (i, cell) in enumerate(sh['W']):
            if i < 4:
                continue
            self.log_pnt(f'{i}:  {cell.value} {varlist["date"]}')
            cell.value = varlist["date"]
        book.save(path)
        self.log_pnt('succeed')
        self.output_summary(book['汇总'])

    def output_summary(self, sheet:openpyxl.worksheet.worksheet):
        ticket = ""
        range = ""
        for (i, item) in enumerate(sheet['H']):
            if i < 30:
                continue
            elif item.value is None:
                break
            print(f'{i} -> {item.value}')
            print(f'{i} -> {i - 29}. {sheet[f"D{i}"].value}')
            ticket += f"{item.value} "
            val = sheet[f"D{i}"].value.replace("\n","")
            content = f'{i - 29}. {val}\n'
            range += content
            # sheet[f[]]
        if ticket != "":
            self.log_pnt(f"制限Redmine票号:\n{ticket}")
            self.log_pnt(f"制限影响范围:\n{range}")
        # print(sheet['H'])

    def thread_newfile(self):
        thread = threading.Thread(target=self.writ_newfile)
        thread.start()

# tbd：提交
    def update_log(self):
        while not self.__q.empty():
            line = self.__q.get()
            self.__log.insert('end', line)
            self.__log.yview('end')
        self.after(500, self.update_log)

    def log_pnt(self, var):
        var_str = f'{str(var)}\n'
        if threading.current_thread == threading.main_thread:
            self.__log.insert('end', var_str)
            # self.__log.config(state='disabled')
            self.__log.yview('end')
        else:
            self.__q.put(var_str)

    def ensure_import(self):
        for (i, item) in enumerate(self.__vars):
            self.log_pnt(f'{i}: {item} -> {self.__vars[item].get()}')
            var_value = self.__vars[item].get()
            varlist[item] = var_value
        self.log_pnt(f'{varlist}')

    def __init__(self):
        super().__init__()
        self.geometry("500x400")
        self.__q = queue.Queue()
        frame1 = tk.Frame(self)
        frame1.pack(fill='x', padx=5)
        # frame1.grid(row=0, column=0, sticky='nsew', padx=(10, 0), pady=(0, 5))
        # self.columnconfigure(0, minsize=50) 
        #part 1
        line = 0
        label = tk.Label(frame1, text="模块id:")
        label.grid(row=line, column=0, sticky='we')
        self.__menu = ttk.Combobox(frame1,  values=getlist(), state="readonly")
        self.__menu.set("")
        self.__menu.grid(row=line, column=1, sticky="we", padx=(0, 10))
        frame1.columnconfigure(index=0,  weight=1)
        frame1.columnconfigure(index=1,  weight=4)
        btn_getfile = tk.Button(frame1, text="copyfile", command=self.getfile)
        btn_getfile.grid(row=line, column=2, sticky='we')

        #part2
        line = 1
        label2 = tk.Label(frame1, text="路径：")
        label2.grid(row=line, column=0, sticky="we")
        self.__var = tk.StringVar()
        self.__var.set('D:/WorkProject/Mecna/01_开发库/22_Release/WeeklyRelease/开发ReleaseCheck/')
        entry = tk.Entry(frame1, textvariable=self.__var)
        entry.grid(row=line, column=1, sticky="we")

        btn_ensure = tk.Button(frame1, text="select", command=self.cmd_btn_ensure)
        btn_ensure.grid(row=line, column=2, sticky="we", padx=(10,0))
        frame1.columnconfigure(index=2,  weight=1)
        frame2 = tk.Frame(self)
        frame2.pack(fill='both', padx=5, pady=5, expand=True)

        line = 2
        labels = {}
        entrys = {}
        self.__vars = {}
        self.__path = ""
        # items = json.load(varlist)
        for (i, item) in enumerate(varlist):
            la = tk.Label(frame1, text=item)
            la.grid(row=line, column=0, sticky='we')
            labels[item] = la
            strVar = tk.StringVar()
            strVar.set(varlist[item])
            self.__vars[item] = strVar
            en = tk.Entry(frame1, textvariable=strVar)
            en.grid(row=line, column=1)
            entrys[item] = en
            # print(f'{i}:  {item}')
            if i == 1:
                btn = tk.Button(frame1, text="ensure import", command=self.ensure_import)
                btn.grid(row=line, column=2, sticky='we')
            elif i == 2:
                btn = tk.Button(frame1, text="save file", command=self.thread_newfile)
                btn.grid(row=line, column=2, sticky='we')
            line += 1

        self.__log = tk.Text(frame2)
        # self.__log.grid(row=1, column=0, sticky='nsew')
        # self.__log.config(state='disabled')
        self.__log.place(relx=0, rely=0, relwidth=0.97, relheight=1)
        scroll = tk.Scrollbar(frame2, width=5)
        scroll.place(relx=0.97, rely=0, relwidth=0.03, relheight=1)
        self.__log.config(yscrollcommand=scroll.set)


if __name__ == "__main__":
    app = Application()
    app.after(500, app.update_log)
    app.mainloop()
    # path = 'D:/WorkProject/Mecna/01_开发库/22_Release/WeeklyRelease/开发ReleaseCheck/20250624_WeeklyRelease\BEV-Step3-CDC(MM)_ReleaseCheck_2.11.2_Solar Charging.xlsx'
    # writ_newfile(path)