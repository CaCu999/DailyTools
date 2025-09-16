import pandas
import os
import time
import threading
import numpy as np
from process import ProgressPublisher

def np_process(raw):
    raw_data = np.frombuffer(raw, dtype=np.uint8)
    total_bytes = len(raw)
    rows = (total_bytes + 15) // 16
    # print(rows)
    # 确保每行都有16个字节
    # 填充剩余的字节
    padded = np.pad(raw_data, (0, rows * 16 - total_bytes), 'constant')
    # padded = np.vectorize(lambda x:f'{x:02x}')(padded)
    padded = np.char.mod('%02x', padded)
    # 转成 n*16的数组
    reshaped = padded.reshape(-1, 16)
    df = pandas.DataFrame(reshaped, columns=[f'Byte {i}' for i in range(1, 17)])
    return df 

def data_thread_process(raw_data_chunk, csv_filename:str, chunk:int, listner:ProgressPublisher = None):
    sem.acquire()
    df = np_process(raw_data_chunk)
    # df.to_csv(csv_filename)
    # dfs.append(df)
    df_dict[chunk] = df
    files.append((csv_filename, df))
    # print(f"CSV file has been created: {csv_filename}")
    global index
    index += 1
    if listner:
        listner.on_progress(index, total_chunks, csv_filename)
    sem.release()

def hex_to_csv(hex_file_path, output_dir, chunk_size=1024*1024, listner:ProgressPublisher = None):
    print("Starting conversion...")
    global sem,index,total_chunks
    sem = threading.Semaphore(4)
    index = 0
    global df_dict, files
    df_dict = {}
    try:
        if not os.path.exists(hex_file_path):
            print(f"Error: The file {hex_file_path} does not exist.")
            return

        start_time = time.time()
        threads = []
        files = []
        dfs = []
        with open(hex_file_path, 'rb') as file:
            file_size = os.path.getsize(hex_file_path)
            total_chunks = (file_size + chunk_size - 1) // chunk_size
            global start_address
            start_address = 0

            for chunk in range(total_chunks):
                file.seek(chunk * chunk_size)
                raw_data_chunk = file.read(min(chunk_size, file_size - chunk * chunk_size))
                csv_filename = os.path.join(output_dir, f'T_hex_data_{chunk}.csv')
                th = threading.Thread(args=(raw_data_chunk, csv_filename, chunk,listner), target=data_thread_process)
                # data_thread_process(raw_data_chunk, csv_filename, chunk)
                threads.append(th)
                th.start()
                start_address += len(raw_data_chunk)
            for t in threads:
                t.join()

            elapsed_time = time.time() - start_time
            print(f"Total processing time: {elapsed_time:.2f} seconds")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    for i in range(len(df_dict)):
        dfs.append(df_dict[i])
    return files, dfs

if __name__ == "__main__":
    import_file = "D:\\DailyWork\\08\\07\\dt\\TRC_CAN.dat"
    out_file = "D:\\Project\\c++\\testPanel\\traceDT2excel\\testOut"
    listner = ProgressPublisher()
    hex_to_csv(import_file, out_file, 10 * 10000, listner)