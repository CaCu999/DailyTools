import pandas
import os
import time
import threading
import numpy as np

def process_data(raw_data_chunk, address, df):
    hex_data = []
    print(f"lens{len(raw_data_chunk)}")
    for i in range(0, len(raw_data_chunk), 16):
        total = len(raw_data_chunk)
        filled = int(i/total/16)
        bar = '=' * filled + '>' + '.' * (100-filled-1)
        precent = (i/total/16) * 100
        print(f'\r[{bar}]{precent:.1f}%', end='')
        hex_line = raw_data_chunk[i:i+16]
        if len(hex_line) < 16:  # 确保每行都有16个字节
            hex_line += b'\x00' * (16 - len(hex_line))  # 填充剩余的字节
        hex_values = [f"{byte:02x}" for byte in hex_line]  # 转换为两位的小写16进制字符串
        address_hex = f"{address + i:08x}"  # 地址为8位小写十六进制格式
        hex_data.append((address_hex,) + tuple(hex_values))
        df.loc[len(df)] = (address_hex,) + tuple(hex_values)
        # print(df.loc[len(df) - 1])
    return hex_data

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



def writ_split_file(csv_filename, raw_data_chunk, start_time):
    cloum = ['Address', 'Byte 1', 'Byte 2', 'Byte 3', 'Byte 4', 'Byte 5', 'Byte 6', 'Byte 7', 'Byte 8', 'Byte 9', 'Byte 10', 'Byte 11', 'Byte 12', 'Byte 13', 'Byte 14', 'Byte 15', 'Byte 16']
    print(f"{csv_filename}\n")
    df = pandas.DataFrame(columns=cloum)
    global start_address
    process_data(raw_data_chunk, start_address, df)
    df.to_csv(csv_filename)
    start_address += len(raw_data_chunk)
    elapsed_time = time.time() - start_time
    print(f"Total processing time: {elapsed_time:.2f} seconds")
    print(f"CSV file has been created: {csv_filename}")

def hex_to_csv(hex_file_path, output_dir, chunk_size=1024*1024):
    print("Starting conversion...")
    try:
        if not os.path.exists(hex_file_path):
            print(f"Error: The file {hex_file_path} does not exist.")
            return

        start_time = time.time()
        threads = []
        files = []
        with open(hex_file_path, 'rb') as file:
            file_size = os.path.getsize(hex_file_path)
            total_chunks = (file_size + chunk_size - 1) // chunk_size
            global start_address
            start_address = 0

            for chunk in range(total_chunks):
                file.seek(chunk * chunk_size)
                csv_filename = os.path.join(output_dir, f'T_hex_data_{chunk}.csv')
                raw_data_chunk = file.read(min(chunk_size, file_size - chunk * chunk_size))
                df = np_process(raw_data_chunk)
                df.to_csv(csv_filename)
                files.append((csv_filename, df))
                start_address += len(raw_data_chunk)
                # print(f"CSV file has been created: {csv_filename}")
                filled = (chunk + 1) * 100 // total_chunks
                precent = (chunk + 1) * 100 / total_chunks
                bar = '=' * filled + '>' + '.' * (100-filled-1)
                print(f'\r[{bar}]{precent:.1f}% {csv_filename}', end='')
            elapsed_time = time.time() - start_time
            print(f"Total processing time: {elapsed_time:.2f} seconds")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    return files

if __name__ == "__main__":
    import_file = "D:\\DailyWork\\08\\07\\dt\\TRC_CAN.dat"
    out_file = "D:\\Project\\c++\\testPanel\\traceDT2excel\\testOut"
    hex_to_csv(import_file, out_file, 10 * 10000 * 16)