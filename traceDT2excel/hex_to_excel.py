import argparse
import os
import time
import shutil
import csv
import threading

def process_data(raw_data_chunk, address):
    hex_data = []
    for i in range(0, len(raw_data_chunk), 16):
        hex_line = raw_data_chunk[i:i+16]
        if len(hex_line) < 16:  # 确保每行都有16个字节
            hex_line += b'\x00' * (16 - len(hex_line))  # 填充剩余的字节
        hex_values = [f"{byte:02x}" for byte in hex_line]  # 转换为两位的小写16进制字符串
        address_hex = f"{address + i:08x}"  # 地址为8位小写十六进制格式
        hex_data.append((address_hex,) + tuple(hex_values))
    return hex_data

def create_backup(filename):
    base, extension = os.path.splitext(filename)
    timestamp = time.strftime("%Y%m%d%H%M%S")
    backup_filename = f"{base}_{timestamp}{extension}"
    shutil.copyfile(filename, backup_filename)
    return backup_filename

def writ_split_file(csv_filename, raw_data_chunk, start_time):
    print(f"{csv_filename}")
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Address', 'Byte 1', 'Byte 2', 'Byte 3', 'Byte 4', 'Byte 5', 'Byte 6', 'Byte 7', 'Byte 8', 'Byte 9', 'Byte 10', 'Byte 11', 'Byte 12', 'Byte 13', 'Byte 14', 'Byte 15', 'Byte 16'])
        global start_address
        hex_data = process_data(raw_data_chunk, start_address)
        for row in hex_data:
            writer.writerow(row)
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
        with open(hex_file_path, 'rb') as file:
            file_size = os.path.getsize(hex_file_path)
            total_chunks = (file_size + chunk_size - 1) // chunk_size
            global start_address
            start_address = 0

            for chunk in range(total_chunks):
                file.seek(chunk * chunk_size)
                csv_filename = os.path.join(output_dir, f'hex_data_{chunk}.csv')
                raw_data_chunk = file.read(min(chunk_size, file_size - chunk * chunk_size))
                th = threading.Thread(args=(csv_filename, raw_data_chunk, start_time), target=writ_split_file, name=f"split{chunk}")
                th.start()
                threads.append(th)
            # with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            #     writer = csv.writer(csvfile)
            #     writer.writerow(['Address', 'Byte 1', 'Byte 2', 'Byte 3', 'Byte 4', 'Byte 5', 'Byte 6', 'Byte 7', 'Byte 8', 'Byte 9', 'Byte 10', 'Byte 11', 'Byte 12', 'Byte 13', 'Byte 14', 'Byte 15', 'Byte 16'])

            #     for chunk in range(total_chunks):
            #         file.seek(chunk * chunk_size)
            #         raw_data_chunk = file.read(min(chunk_size, file_size - chunk * chunk_size))
            #         hex_data = process_data(raw_data_chunk, start_address)
            #         for row in hex_data:
            #             writer.writerow(row)
            #         start_address += len(raw_data_chunk)

            #     elapsed_time = time.time() - start_time
            #     print(f"Total processing time: {elapsed_time:.2f} seconds")
            #     print(f"CSV file has been created: {csv_filename}")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert hex dump to CSV file.')
    parser.add_argument('hex_file_path', nargs='?', default='TRC_CAN.dat', help='Path to the hex dump file.')
    parser.add_argument('output_dir', nargs='?', default='.', help='Output directory for CSV files.')
    
    args = parser.parse_args()

    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)  # Ensure the output directory exists

    hex_to_csv(args.hex_file_path, args.output_dir, chunk_size=20 * 1024 * 1024)