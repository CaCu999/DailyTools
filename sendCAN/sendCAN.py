import json
import os
from canlib import canlib, Frame
import time
from cantools import database

configpath = os.path.join(os.path.dirname(__file__), "CANconfig.json")
with open(configpath) as f:
    config = json.load(f)
print(configpath)
# config = json.load("testPanel\CANconfig.json")
print(config["CANConfig"][0])
canConfig = config["CANConfig"]
inter1 = canConfig[0]["interface"]
ch1 = canConfig[0]["channel"]
app_name1 = canConfig[0]["app_name"]
bitrate0 = canConfig[0]["bitrate"]
tseg1_0 = canConfig[0]["tseg1"]
tseg1_0 = canConfig[0]["tseg2"]
data_bitrate = canConfig[0]["data_bitrate"]
fd0 = canConfig[0]["fd"]

# # 创建CAN总线对象
# bus = can.interface.Bus(interface = inter1, channel = int(ch1), 
#           receive_own_messages = True, app_name = app_name1)
# msg1 = can.Message(arbitration_id=0x440, data=[0x40, 0x40, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00])
# msg2 = can.Message(arbitration_id=0x445, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
# bus.send_periodic(msg1, 1000)
# bus.send_periodic(msg2, 1000)
# print(f"sent frame id: {msg1.arbitration_id}, Data: {msg1.data}")
# print(f"sent frame id: {msg2.arbitration_id}, Data: {msg2.data}")
channel_number = 0
chd = canlib.ChannelData(channel_number)
print("%d. %s (%s / %s) " % (channel_number,
                             chd.channel_name,
                             chd.card_upc_no,
                             chd.card_serial_no))
ch = canlib.openChannel(channel_number,flags=canlib.canOPEN_ACCEPT_VIRTUAL)
ch.setBusParams(canlib.canBITRATE_500K, 0, 0, 0, 0, canlib.canFD_BITRATE_2M_80P)
print("Going on bus")
ch.busOn()
frame = Frame(id_ = 0x445,
              data = [0,0,0,0, 0,0,0,0],
              dlc=0,
              flags=0)
frame2 = Frame(id_ = 0x440,
               data = [0x40, 0x40, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00],
               dlc=8,
               flags=0)
frame3 = Frame(id_=0x2A6,
               data = [0x00, 0x00, 0x0d, 0x32, 0x01, 0xFF, 0x01, 0xFF, 
                       0x00, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                       0x00, 0x00, 0x01, 0xFF, 0x01, 0xFF, 0xFF, 0xFF, 
                       0x01, 0xFF, 0xFE, 0x00, 0x00, 0x00, 0x00, 0x00],
                dlc = 32,
                flags=0)
ch.write(frame)
ch.write(frame2)
ch.write(frame3)
# ch.write(frame2)
print("Waiting for incoming messages....")
while True:
    recv_frame = ch.read(timeout=1000)
    if recv_frame:
        print(f"recv message {recv_frame}")
        
        print(f" flags {recv_frame.flags & canlib.MessageFlag.ERROR_FRAME}")
        print(f" flags {recv_frame.flags & canlib.MessageFlag.OVERRUN}")
    else:
        print(f"no incoming message")
    time.sleep(0.001)
