from canlib import canlib, Frame
import time
# 加载DBC文件
from canlib.kvadblib import dbc
import os

# 初始化CANlib库
# canlib.init()

# 打开通道
ch = canlib.openChannel(
    channel=1,  # 使用第一个通道
    flags=canlib.Open.ACCEPT_LARGE_DLC,  
    bitrate=canlib.canFD_BITRATE_2M_80P
)
# 设置CAN驱动模式为正常
ch.setBusOutputControl(canlib.Driver.NORMAL)

# 激活CAN芯片
ch.busOn()
# dbcpath = "D:\\BasicSetting\\dbc\\excel2dbc-GlobalCAN_19PFv3-GCANID_T.dbc"
dbcpath = "D:\\BasicSetting\\dbc\\step3\\CDC_Multi-Media_system_CAN_Com_spec_BA_CAN_2M1_v6.20_DSV240706.dbc"
# dbc = database.load_file(dbcpath)
dbcFile = dbc.Dbc(filename=dbcpath)

frame = Frame(id_ = 0x445,
              data = [0,0,0,0, 0,0,0,0],
              dlc=0,
              flags=0)
frame2 = Frame(id_ = 0x440,
               data = [0x40, 0x40, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00],
               dlc=8,
               flags=0)
frame3 = Frame(id_ = 0x1E3,
               data = [0x00, 0x00, 0x7e, 0x00, 0x00, 0x00, 0x00, 0x00],
               dlc=32,
               flags=canlib.MessageFlag.EXT)
# 获取消息
message = dbcFile.get_message_by_name("PLG1G16")
# # 获取信号
signal = message.get_signal_by_name("P_TMRAVA")
m = message.bind()
m.P_TMRAVA.phys = 2
print(m._frame)
# print(signal.type)
# signal.value = 2
# print(signal.phys_from)
# print(message.asframe)
# message.data = signal.value.to_bytes(signal.size.length, byteorder='little')
# print(message.data)
# print(message.asframe())
# # 创建CAN帧
# frame = message.asframe()
# frame.data

# # 创建CAN帧
frame4 = m._frame
frame4.flags = canlib.MessageFlag.EXT
while True:
    # print(frame)
    # 发送CAN帧
    ch.write(frame)
    print(ch.read())
    ch.write(frame2)
    ch.write(frame3)
    time.sleep(1)

# # 等待最多500毫秒直到消息发送完成
# ch.writeSync(timeout=500)

# 禁用CAN芯片
ch.busOff()

# 关闭通道
ch.close()

# # 释放CANlib资源
# canlib.release()