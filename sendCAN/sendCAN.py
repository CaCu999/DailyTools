import json
import os
from canlib import canlib, Frame
import time
from cantools import database

configpath = os.path.join(os.path.dirname(__file__), "file", "CANconfig.json")
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
# ch.setBusParams(canlib.canBITRATE_500K, 0, 0, 0, 0, canlib.canFD_BITRATE_2M_80P)
print("Going on bus")
# ch.busOn()
# frame = Frame(id_ = 0x445,
#               data = [0,0,0,0, 0,0,0,0],
#               dlc=0,
#               flags=0)
# frame2 = Frame(id_ = 0x440,
#                data = [0x40, 0x40, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00],
#                dlc=8,
#                flags=0)
# dbcpath = os.path.join(os.path.dirname(__file__), "file", "global-2M.dbc")
dbcpath = "D:\\BasicSetting\\dbc\\excel2dbc-GlobalCAN_19PFv3-GCANID_T.dbc"
dbc = database.load_file(dbcpath)
res = dbc.get_message_by_name("PLG1G17")
signal = res.get_signal_by_name("P_TMRAVA")
print(f'{signal.value}')
raw_value = 2
buffer = bytearray(8)
print(signal.byte_order)
buffer.extend(raw_value.to_bytes(length=signal.length, byteorder='big'))
frame_cus = Frame(id_ = res.frame_id, data=buffer)
print(frame_cus.data)
# print(dbc)
# ch.write(frame)
# ch.write(frame2)
if len(frame_cus.data) == 0:
    print("帧ID或数据为空!")
    # 处理这种情况

ch.write(frame_cus)

# # ch.write(frame2)
print("Waiting for incoming messages....")
while True:
    try:
        recv_frame = ch.read(timeout=1000)
    except Exception as e:
        print(f"err {e}")
        break

    if recv_frame:
        print(f"recv message {recv_frame}")
        
        print(f" flags {recv_frame.flags & canlib.MessageFlag.ERROR_FRAME}")
        print(f" flags {recv_frame.flags & canlib.MessageFlag.OVERRUN}")
    else:
        print(f"no incoming message")
    time.sleep(0.001)
