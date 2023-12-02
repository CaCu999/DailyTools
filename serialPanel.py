import serial

# 创建一个串口实例
ser = serial.Serial(
    port='COM7',  # 串口号
    baudrate=9600,  # 波特率
    rtscts=True,  # 开启 RTS/CTS 流控制
    dsrdtr=True,  # 开启 DSR/DTR 流控制
)

while True:
    data = ser.readline()  # 读取一行数据
    print(ser.read())  # 打印数据
    data = data.decode('utf-8')  # 将二进制数据解码为ASCII
    print(data)  # 打印数据
