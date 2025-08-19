# from hex_to_excel import hex_to_csv
from hex2excel import hex_to_csv
import os
import pandas
from datetime import datetime
from datetime import timedelta
import threading
import numpy as np

# 前3个字节是TICKCOUT， 第四个字节是F0, 后面6个字节，年月日十分秒，2个字节tripcount, 1个字节gps时间同步状态，1个字节gps时间帧记录的原因，2个字节0x00
# 启动会后第一条F0的数据帧是0x00, 0x00 ，0x00开头， DiagnosticRecorder开关打开，第四个字节是F2的数据帧，后面也会紧跟一条F0的时间帧，这个条前三个字节不是0x00
# 比如这样
# GPS时间同步的log:       00 00 1C F0 24 06 26 08 10 23 00 00 00 00 00 00 ①
# 当前记录的log:          00 04 7C 38 10 00 00 08 00 00 00 00 00 00 00 00 ②
# 那可以通过①得到系统时间 2024/6/26 8:10:23,当时的系统tickcount是0x00001C
# log②的系统时间tickcout是0x00047C， 这样相对①的时间偏移是0x00047C - 0x00001C = 0x460
# 0x460转成10进制1120，再乘以50，就是56000ms = 56s，那log②的时间就是2024/6/26 8:12:19

def safe_clean_convert(x):
    cleaned = str(x).strip()
    return f'{int(cleaned, 16):02X}'

def get_content(line_index, start, bitNum, df):
    content = " "
    sec_line = df.loc[line_index]
    content += " ".join([safe_clean_convert(sec_line[f'Byte {i}']) for i in range(start, start + bitNum)])
    return content

def np_split(df:pandas.DataFrame):
    mark = 'F0'
    col_mark = df.columns[3]
    condition = (df[col_mark] == mark)
    time_cols = df.columns[4:9]
    time_str = df[time_cols].astype(str).apply(lambda x: ''.join(x), axis = 1)
    times = time_str.apply(datetime.strptime())
    split_indices = np.where()

def getTICKCOUT(dir, fn:str):
    path = os.path.join(dir, fn)
    print(f'start {path}')
    out = fn.replace('.csv','') + "_out.csv"
    df = pandas.read_csv(path)
    dt  = datetime(2001, 1, 1)
    pretick = 0
    df["raw_value"]=""
    df["tickout"] = ""
    df["date"] = ""
    df["time"] = ""
    df["message"] = ""
    df["len"] = ""
    df["content"] = ""
    for idx, row in df.iterrows():
        # if idx > 150:
        #     break
        raw_value = [safe_clean_convert(row[f'Byte {i}']) for i in range(1,17)]
        res = int(raw_value,16)
        df.loc[idx, 'raw_value'] = " ".join(raw_value)
        combine_three = "".join(raw_value[:3])
        # print(combine_three)
        tickout = int(combine_three, 16) * 50
        if tickout == 0:
            dt = datetime(2001, 1, 1)
            pretick = 0
        if raw_value[3] == 'F0':
            try:
                year = int(raw_value[4])
                mon = int(raw_value[5])
                day = int(raw_value[6])
                hour = int(raw_value[7])
                min = int(raw_value[8])
                sec = int(raw_value[9])
                if year > 20:
                    dt = datetime(year, mon, day, hour, min, sec)
                    print(f"{dt}")
                print(f'{year} {mon} {min}')
            except ValueError as e:
                print(f'{raw_value[5:10]}')
        else:
            canid = f'0x{raw_value[3]}{raw_value[4]}'
            df.loc[idx, "message"] = f'[CAN ID:{canid}]'
            df.loc[idx, "len"] = f"{raw_value[7]}"
            content = " ".join(raw_value[8:])
            sig_len = int(raw_value[7], 16)
            if sig_len == 32 or sig_len == 64:
                num = sig_len - 8
                line_index = 1
                while num > 0:
                    len = 13 if num > 13 else num
                    content += get_content(idx + line_index, 4, len, df)
                    num -= len
                    line_index += 1
            df.loc[idx, "content"] = content

            
        diffTick = tickout - pretick
        pretick = tickout
        dt = dt + timedelta(milliseconds=diffTick)
        df.loc[idx,"tickout"] = f'[{int(tickout/1000):06X}.{tickout%1000}s]'
        df.loc[idx, "date"] = dt.strftime("%Y/%m/%d")
        df.loc[idx, "time"] = dt.strftime("%H:%M:%S")
        # strr = f"{combine_three}\t{df.loc[idx, 'tickout']}\t{df.loc[idx, 'date']}\t{df.loc[idx, 'time']}"
        # print(f"{strr}")
    exportPath = os.path.join(dir, out)
    df.to_csv(exportPath)
    print(f'end save {exportPath}')
    # print(exportPath)



if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='Convert hex dump to CSV file.')
    # parser.add_argument('hex_file_path', nargs='?', default='TRC_CAN.dat', help='Path to the hex dump file.')
    # parser.add_argument('output_dir', nargs='?', default='.', help='Output directory for CSV files.')
    
    # args = parser.parse_args()

    # if args.output_dir:
    #     os.makedirs(args.output_dir, exist_ok=True)  # Ensure the output directory exists

    import_file = "D:\\DailyWork\\08\\07\\dt\\TRC_CAN.dat"
    out_file = "D:\\Project\\c++\\testPanel\\traceDT2excel\\testOut"
    # # # hex_to_csv(args.hex_file_path, args.output_dir)
    files = hex_to_csv(import_file, out_file, 100 * 10000 * 16)
    print(f'end.... {files}')
    # out = "TRC_CAN_1.csv"
    # getTICKCOUT(out_file, out)
    threads = []
    for (f,df) in files:
        name = os.path.basename(f)
        th = threading.Thread(args=(out_file, name), target=getTICKCOUT)
        threads.append(th)
        th.start()
        # getTICKCOUT(out_file, name)
    for t in threads:
        t.join()
    
