import tkinter as tk
import os
import json

def loadFile(path):
    global js
    with open(path) as f:
        js = json.load(f)
    print(js)

def trans():
    input = inputVar.get()
    if input == "":
        outputVar.set("intput string is null")
    else:
        for key,val in js.items():
            print(f"{key} : {val} _{input}__ {input.__contains__(key)}")
            if input.__contains__(key):
                input = input.replace(key, val)
                if input.startswith("\\\\"):
                    input = input.replace("/", "\\")
                else:
                    input = input.replace("\\", "/")
                outputVar.set(input)
                window.clipboard_clear()
                window.clipboard_append(input)
                window.update()
                break
            else:
                outputVar.set("not found all")

def clear():
    inputVar.set("")
    outputVar.set("")

def mainWindow():
    global window
    window = tk.Tk()
    window.geometry("600x200")
    window.title("路径转换")
    #输入控件设置
    global inputVar,outputVar
    inputVar = tk.StringVar()
    input = tk.Entry(window, textvariable=inputVar)
    inputLabel = tk.Label(text="输入路径：")
    inputBtn = tk.Button(text="转化", width=10, command=trans)
    inputLabel.grid(row=0, column=0, padx=5, pady=5)
    input.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    inputBtn.grid(row=0, column=2, padx=5, pady=5)
    #输出控件设置
    outputVar = tk.StringVar()
    output = tk.Entry(window, textvariable=outputVar)
    outputLabel = tk.Label(text="输出路径：")
    outputLabel.grid(row=1, column=0, padx=5, pady=5)
    output.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    #行列设置
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=5)
    window.columnconfigure(2, weight=1)
    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)
    # print(os.path.dirname(__file__))
    path = os.path.join(os.path.dirname(__file__),"file",  "path.json")
    # print(path)
    #按钮
    clrBtn = tk.Button(text="清空", command=clear, width=10)
    clrBtn.grid(row=1, column=2, padx=5, pady=5)
    loadFile(path)
    window.mainloop()

if __name__ == "__main__":
    mainWindow()