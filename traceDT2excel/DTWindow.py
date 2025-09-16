import tkinter as tk
from tkinter import filedialog
import DT2excel
from hex2excel import hex_to_csv
import pandas
import threading
import time
import os
from concurrent.futures import ProcessPoolExecutor
from process import ProgressPublisher
from process import EventLisnter
from tkinter import ttk

def file_select():
    res = filedialog.askopenfilename()
    global input_str
    input_str.set(res)

def dir_select():
    res = filedialog.askdirectory()
    global output_str
    output_str.set(res)

def DTTrans():
    start = time.time()
    import_file = input_str.get()
    out_file = output_str.get()
    files,dfs = hex_to_csv(import_file, out_file, 100 * 10000, fileListener)
    df = pandas.concat(dfs, ignore_index=True)
    # print(df)
    res = DT2excel.np_split(df)
    print('#####################################################################')
    global total, index
    total = len(res)
    index = 0
    print(f"table num{len(res)}")
    DT2excel.thread_TICKOUT(res, out_file, excelListener)
    
    elapsed_time = time.time() - start
    print(f"Total processing time: {elapsed_time:.2f} seconds")

def btn_click():
    global btn_trans
    btn_trans.config(state='disabled')
    thread = threading.Thread(target=DTTrans)
    thread.start()

def DTWindow():
    window = tk.Tk()
    window.geometry("500x400")
    
    panel1 = tk.Frame(window)
    panel1.grid(row=0, column=0, sticky='nsew')
    window.rowconfigure(index=0, weight=2)
    window.rowconfigure(index=1, weight=1)
    window.rowconfigure(index=2, weight=1)
    window.rowconfigure(index=3, weight=1)
    window.rowconfigure(index=4, weight=1)
    window.columnconfigure(index=0, weight=1)
    lb_input = tk.Label(panel1, text="输入文件")
    lb_input.grid(row=0, column=0)
    global input_str
    input_str = tk.StringVar()
    entry_in = tk.Entry(panel1, textvariable=input_str)
    entry_in.grid(row=0, column=1, sticky='we')
    btn_input = tk.Button(panel1, text="ensure", command=file_select)
    btn_input.grid(row=0, column=2)

    lb_output = tk.Label(panel1, text="输出路径")
    lb_output.grid(row=1, column=0, sticky='nsew')
    global output_str
    output_str = tk.StringVar()
    entry_out = tk.Entry(panel1, textvariable=output_str)
    entry_out.grid(row=1, column=1, sticky='we')
    btn_output = tk.Button(panel1, text="ensure", command=dir_select)
    btn_output.grid(row=1, column=2)
    panel1.columnconfigure(index=0, weight=1)
    panel1.columnconfigure(index=1, weight=6)
    panel1.columnconfigure(index=2, weight=1)
    panel1.rowconfigure(index=0, weight=1)
    panel1.rowconfigure(index=1, weight=1)

    panel2 = tk.Frame(window)
    panel2.grid(row=1, column=0)
    global btn_trans
    btn_trans = tk.Button(panel2, text="输出DTlog", command=btn_click)
    panel2.columnconfigure(index=0, weight=2)
    panel2.columnconfigure(index=1, weight=4)
    panel2.columnconfigure(index=2, weight=2)
    btn_trans.grid(row=0, column=2)

    panel3 = tk.Frame(window)
    panel3.grid(row=2, column=0,sticky='wen',padx=10)
    panel3.columnconfigure(index=0, weight=1)
    panel3.columnconfigure(index=1, weight=8)
    panel3.columnconfigure(index=2, weight=1)
    label_file = tk.Label(panel3, text="文件读取")
    label_file.grid(row=0, column=0, sticky='w')
    pro_file_var = tk.IntVar()
    pro_file = ttk.Progressbar(panel3, variable=pro_file_var, orient="horizontal", length=100, mode='determinate')
    pro_file.grid(row=0, column=1, sticky='we')
    label_file_pro = tk.Label(panel3, textvariable=pro_file_var)
    label_file_pro.grid(row=0, column=2)

    panel4 = tk.Frame(window)
    panel4.grid(row=3, column=0,sticky='wen',padx=10)
    panel4.columnconfigure(index=0, weight=1)
    panel4.columnconfigure(index=1, weight=8)
    panel4.columnconfigure(index=2, weight=1)
    label_excel = tk.Label(panel4, text="内容解析")
    label_excel.grid(row=0, column=0, sticky='w')
    pro_excel_var = tk.IntVar()
    pro_excel = ttk.Progressbar(panel4, variable=pro_excel_var, orient="horizontal", length=100, mode='determinate')
    pro_excel.grid(row=0, column=1, sticky='we') 
    label_file_excel = tk.Label(panel4, textvariable=pro_excel_var)
    label_file_excel.grid(row=0, column=2)
    eventListner = EventLisnter(window)
    global fileListener,excelListener
    fileListener = ProgressPublisher()
    fileListener.add_listener(eventListner)
    eventListner.add_progress(pro_file_var, fileListener)
    excelListener =  ProgressPublisher()
    eventListner.add_progress(pro_excel_var, excelListener)
    excelListener.add_listener(eventListner)
    eventListner.add_btn(btn_trans, excelListener)
    return window


        

if __name__ == "__main__":
    app = DTWindow()

    app.mainloop()

