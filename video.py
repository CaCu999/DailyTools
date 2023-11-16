import subprocess
from datetime import datetime
import os
import tkinter as tk
from tkinter import filedialog
import tkinter.ttk
import threading
import shutil

window = tk.Tk()

def get_num(filepath):
    command = f"ffprobe -v error "
    command += f"-show_entries format=duration "
    command += f"-of default=noprint_wrappers=1:nokey=1 -sexagesimal {filepath}"
    print(command)
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    output = process.stdout.readline()
    output = output.strip().decode()
    tt = datetime.strptime(output, '%H:%M:%S.%f')
    seconds = tt.hour * 3600 + tt.minute * 60 + tt.second + 1
    return seconds

def split_video(filepath):
    dir = os.path.dirname(filepath)
    dir = os.path.join(dir, 'tmp')
    if not os.path.exists(dir):
        os.mkdir(dir)
    command = f'ffmpeg -i {filepath} -r 1 {dir}/test_%04d.png'
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    while process.poll() is None:
        line = process.stdout.readline()

def merge_video(filepath):
    dir = os.path.dirname(filepath)
    tmp = os.path.join(dir, 'tmp')
    filename = var_filename.get() or "output"
    filename = os.path.join(dir, filename + ".mp4")
    if os.path.exists(filename):
        os.remove(filename)
    command = f"ffmpeg -i {tmp}/test_%04d.png -c:v libx264 -r 10 {filename}"
    process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    while process.poll() is None:
        line = process.stdout.readline()
    global is_done
    is_done = True
    if os.path.exists(tmp):
        shutil.rmtree(tmp)

def ensure():
    global is_done
    if not is_done:
        return
    is_done = False
    path = var_path.get()
    process_bar['value'] = 0
    var_value.set('00.00%')
    split_video(path)
    merge_video(path)

def func_thread():
    thread = threading.Thread(target=ensure)
    thread.daemon = True
    thread.start()

def askfile():
    global var_path
    var_path.set(filedialog.askopenfilename())
    global all_num
    all_num = get_num(var_path.get())

def show_process():
    window.after(100, show_process)
    if is_done:
        var_value.set("done !!!!")
        return
    elif var_path.get() == "":
        var_value.set(f"no path")
        return
    elif process_bar['value'] == 100:
        var_value.set("merging video...")
        return
    path = os.path.dirname(var_path.get())
    path = os.path.join(path, "tmp")
    if not os.path.exists(path):
        return
    num = len(os.listdir(path))
    process_bar['value'] = min(int(num * 100 / all_num),100)
    var_value.set(f'%.2f'%min(float(num * 100 / all_num),100) + "%")

def mainWindow():
    global all_num,is_done
    is_done = True
    all_num = 0
    window.geometry("400x250")
    #path
    label_path = tk.Label(window, text='path')
    label_path.place(relwidth=0.2, relheight=0.15, relx=0.01, rely=0.1)
    global var_path,var_value,var_filename,process_bar
    var_path = tk.StringVar()
    entity_path = tk.Entry(window, textvariable=var_path)
    entity_path.place(relwidth=0.55, relheight=0.15, relx=0.201, rely=0.1)
    button_path = tk.Button(window, text="select", command=askfile)
    button_path.place(relwidth=0.15, relheight=0.15, relx=0.8, rely=0.1)

    #filename 
    label_filename = tk.Label(window, text="filename")
    label_filename.place(relwidth=0.2, relheight=0.15, relx=0.01, rely=0.3)
    var_filename = tk.StringVar()
    entity_filename = tk.Entry(window, textvariable=var_filename)
    entity_filename.place(relwidth=0.55, relheight=0.15, relx=0.201, rely=0.3)
    button_ensure = tk.Button(window, text="ensure", command=func_thread)
    button_ensure.place(relwidth=0.15, relheight=0.15, relx=0.8, rely=0.3)

    #process
    label_process = tk.Label(window, text="process")
    label_process.place(relwidth= 0.2, relheight=0.15, relx= 0.01, rely=0.5)
    var_value = tk.StringVar()
    entity_value = tk.Entry(window, text=var_value)
    entity_value.place(relwidth= 0.3, relheight=0.15, relx= 0.25, rely=0.5)
    process_bar = tkinter.ttk.Progressbar(window)
    process_bar.place(relwidth=0.9, relheight= 0.05, relx=0.05, rely=0.7)
    process_bar['maximum'] = 100
    window.after(100, show_process)
    window.mainloop()

if __name__ == "__main__":
    filepath = "D:\DailyWork\\11\\16\\test.mov"
    # get_num(filepath)
    # split_video(filepath)
    # merge_video(filepath)
    mainWindow()