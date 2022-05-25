from enum import Enum


class TLVS(Enum):
    """
    Enum of TLV types
    """
    SOURCE_ADDRESS = 0
    MODE = 1
    TIMEOUT = 2
    CHALLENGE = 3
    RESPONSE = 4
    LINK_LAYER_FRAME_COUNTER = 5
    LINK_QUALITY = 6
    NETWORK_PARAMETER = 7
    MLE_FRAME_COUNTER = 8
    ROUTE64 = 9
    ADDRESS16 = 10
    LEADER_DATA = 11
    NETWORK_DATA = 12
    TLV_REQUEST = 13
    SCAN_MASK = 14
    CONNECTIVITY = 15
    LINK_MARGIN = 16
    STATUS = 17
    VERSION = 18
    ADDRESS_REGISTRATION = 19
    CHANNEL = 20
    PAN_ID = 21
    ACTIVE_TIMESTAMP = 22
    PENDING_TIMESTAMP = 23
    ACTIVE_OPERATIONAL_DATASET = 24
    PENDING_OPERATIONAL_DATASET = 25
    THREAD_DISCOVERY = 26
    UNKNOWN = -1

    def __str__(self):
        return self.name

    @classmethod
    def get_by_value(cls, value):
        """
        Get enum by value
        """
        for tlv in cls.__members__.values():
            if tlv.value == value:
                return tlv
        return cls.UNKNOWN
