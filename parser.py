import pathlib
from commands import Commands
from tlvs import TLVS


def read_file(file_name: pathlib.Path) -> bin:
    """Open file as binary and return the data."""
    with open(file_name, "rb") as file:
        data = file.read()
    return data


def print_hex(data: bin) -> str:
    """Print a string as hexadecimal."""
    return " ".join(["{:02X}".format(x) for x in data])


def assign_command_type(message: bin, res=None) -> list:
    """
    Assign the command type and the TLV names to the message.
    :param res:
    :param message:
    :return: command and tlvs
    """

    if res is None:
        res = []
    if message == b'':
        return res
    if message[0:1] == b'\xFF':
        command_type = message[1:2]
        next_message_index, tlvs = get_tlvs(message[2:])
        if next_message_index is not None:
            next_message_index += 2
    else:
        command_type = message[11:12]
        next_message_index, tlvs = get_tlvs(message[12:])
        if next_message_index is not None:
            next_message_index += 12
    if command_type == b'\x00':
        command = Commands.LINK_REQUEST
    elif command_type == b'\x01':
        command = Commands.LINK_ACCEPT
    elif command_type == b'\x02':
        command = Commands.LINK_ACCEPT_AND_REQUEST
    elif command_type == b'\x03':
        command = Commands.LINK_REJECT
    elif command_type == b'\x04':
        command = Commands.ADVERTISEMENT
    elif command_type == b'\x05':
        command = Commands.UPDATE
    elif command_type == b'\x06':
        command = Commands.UPDATE_REQUEST
    elif command_type == b'\x07':
        command = Commands.DATA_REQUEST
    elif command_type == b'\x08':
        command = Commands.DATA_RESPONSE
    elif command_type == b'\x09':
        command = Commands.PARENT_REQUEST
    elif command_type == b'\x0A':
        command = Commands.PARENT_RESPONSE
    elif command_type == b'\x0B':
        command = Commands.CHILD_ID_REQUEST
    elif command_type == b'\x0C':
        command = Commands.CHILD_ID_RESPONSE
    elif command_type == b'\x0D':
        command = Commands.CHILD_UPDATE_REQUEST
    elif command_type == b'\x0E':
        command = Commands.CHILD_UPDATE_RESPONSE
    elif command_type == b'\x0F':
        command = Commands.ANNOUNCE
    elif command_type == b'\x10':
        command = Commands.DISCOVERY_REQUEST
    elif command_type == b'\x11':
        command = Commands.DISCOVERY_RESPONSE
    else:
        command = Commands.UNKNOWN

    res.append({"Name":command, **{"tlvs": tlvs}, **{"total_message": print_hex(message[0:next_message_index])}})
    if next_message_index is not None:
        return assign_command_type(message[next_message_index:], res)
    else:
        return res


def get_tlvs(msg: bin, next_index=0, res=None) -> (int, list):
    """
    Parse the message and return a list of TLVs.
    :param next_index: the index of the next message
    :param msg: binary TLV data
    :param res: list of TLVs. Initialized to none
    :return: list of all TlVs in the message
    """
    # The message can have several TLV's and we'll return a list of all TLV's in the message.
    type_loc = 0
    length_loc = 1
    if res is None:
        res = []
    if msg == b'':
        return None, res
    if msg[0:1] == b'\xFF' or msg[0:2] == b'\x00\x15':
        return next_index, res
    if msg[type_loc] == 0:
        # Source Address TLV
        tlv_type = TLVS.SOURCE_ADDRESS
    elif msg[type_loc] == 1:
        # Mode TLV
        tlv_type = TLVS.MODE
    elif msg[type_loc] == 2:
        # Timeout TLV
        tlv_type = TLVS.TIMEOUT
    elif msg[type_loc] == 3:
        # Challenge TLV
        tlv_type = TLVS.CHALLENGE
    elif msg[type_loc] == 4:
        # Response TLV
        tlv_type = TLVS.RESPONSE
    elif msg[type_loc] == 5:
        # Link-layer Frame Counter TLV
        tlv_type = TLVS.LINK_LAYER_FRAME_COUNTER
    elif msg[type_loc] == 6:
        # Link Quality TLV
        tlv_type = TLVS.LINK_QUALITY
    elif msg[type_loc] == 7:
        # Network Parameter TLV
        tlv_type = TLVS.NETWORK_PARAMETER
    elif msg[type_loc] == 8:
        # MLE Frame Counter TLV
        tlv_type = TLVS.MLE_FRAME_COUNTER
    elif msg[type_loc] == 9:
        # Route64 TLV
        tlv_type = TLVS.ROUTE64
    elif msg[type_loc] == 10:
        # Address16 TLV
        tlv_type = TLVS.ADDRESS16
    elif msg[type_loc] == 11:
        # Leader Data TLV
        tlv_type = TLVS.LEADER_DATA
    elif msg[type_loc] == 12:
        # Network Data TLV
        tlv_type = TLVS.NETWORK_DATA
    elif msg[type_loc] == 13:
        # TLV Request TLV
        tlv_type = TLVS.TLV_REQUEST
    elif msg[type_loc] == 14:
        # Scan Mask TLV
        tlv_type = TLVS.SCAN_MASK
    elif msg[type_loc] == 15:
        # Connectivity TLV
        tlv_type = TLVS.CONNECTIVITY
    elif msg[type_loc] == 16:
        # Link Margin TLV
        tlv_type = TLVS.LINK_MARGIN
    elif msg[type_loc] == 17:
        # Status TLV
        tlv_type = TLVS.STATUS
    elif msg[type_loc] == 18:
        # Version TLV
        tlv_type = TLVS.VERSION
    elif msg[type_loc] == 19:
        # Address Registration TLV
        tlv_type = TLVS.ADDRESS_REGISTRATION
    elif msg[type_loc] == 20:
        # Channel TLV
        tlv_type = TLVS.CHANNEL
    elif msg[type_loc] == 21:
        # PAN ID TLV
        tlv_type = TLVS.PAN_ID
    elif msg[type_loc] == 22:
        # Active Timestamp TLV
        tlv_type = TLVS.ACTIVE_TIMESTAMP
    elif msg[type_loc] == 23:
        # Pending Timestamp TLV
        tlv_type = TLVS.PENDING_TIMESTAMP
    elif msg[type_loc] == 24:
        # Active Operational Dataset TLV
        tlv_type = TLVS.ACTIVE_OPERATIONAL_DATASET
    elif msg[type_loc] == 25:
        # Pending Operational Dataset TLV
        tlv_type = TLVS.PENDING_OPERATIONAL_DATASET
    elif msg[type_loc] == 26:
        # Thread Discovery TLV
        tlv_type = TLVS.THREAD_DISCOVERY
    else:
        tlv_type = TLVS.UNKNOWN
    tlv_length = msg[length_loc]
    tlv_value = msg[length_loc + 1:2 + tlv_length]
    res.append({"type": tlv_type, "length": tlv_length, "value": tlv_value})

    next_index += tlv_length + 2

    return get_tlvs(msg[tlv_length + 2:], next_index, res)


if __name__ == '__main__':
    bb_file = pathlib.Path("test.bin")

    bb_msg = assign_command_type(read_file(bb_file))
    for msg in bb_msg:
        print(msg["name"])
        print(msg["total_message"])
        print()