from tkinter import filedialog
import pandas as pd
import os
import json

def mainWindow():
    file = filedialog.askopenfilename(filetypes= [("all files", "*.csv")])
    sh = os.path.basename(file)
    print(file)
    print(sh)
    with open("testPanel\logSymbol.json") as f:
        data = json.load(f)
    print(data)
    with open("testPanel\propSymbol.json") as f:
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
            time = row['DATE_TIME'] 
            log_data = row['LOG_DATA']
            func = data[log_data.split("|")[0]]
            content = log_data.split("|")[1]
            content = content.replace("DynamicData:","")
            content = content if prop.get(content) is None else prop[content]
            line = f"{time} {func}: {content}\n"
            f.write(line)
            print(line)
        

if __name__ == "__main__":
    mainWindow()



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