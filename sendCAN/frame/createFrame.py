from cantools import database
from canlib import Frame
from cantools.typechecking import ByteOrder
import cantools

def create_buffer_from_message(msg: database.can.message.Message) -> bytearray:
    buffer = bytearray(msg.length)
    return buffer

def change_value_in_buffer(buffer: bytearray,
                           signal: database.can.signal.Signal,
                           value: int):
    # order = 'litter' if signal.byte_order == 'little_endian'
    buffer.extend(value.to_bytes(signal.length))