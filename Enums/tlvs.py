from enum import Enum


class TLVS(Enum):
    """
    Enum of TLV types
    """
    SOURCE_ADDRESS_TLV = 0
    MODE_TLV = 1
    TIMEOUT_TLV = 2
    CHALLENGE_TLV = 3
    RESPONSE_TLV = 4
    LINK_LAYER_FRAME_COUNTER_TLV = 5
    LINK_QUALITY_TLV = 6
    NETWORK_PARAMETER_TLV = 7
    MLE_FRAME_COUNTER_TLV = 8
    ROUTE64_TLV = 9
    ADDRESS16_TLV = 10
    LEADER_DATA_TLV = 11
    NETWORK_DATA_TLV = 12
    TLV_REQUEST_TLV = 13
    SCAN_MASK_TLV = 14
    CONNECTIVITY_TLV = 15
    LINK_MARGIN_TLV = 16
    STATUS_TLV = 17
    VERSION_TLV = 18
    ADDRESS_REGISTRATION_TLV = 19
    CHANNEL_TLV = 20
    PAN_ID_TLV = 21
    ACTIVE_TIMESTAMP_TLV = 22
    PENDING_TIMESTAMP_TLV = 23
    ACTIVE_OPERATIONAL_DATASET_TLV = 24
    PENDING_OPERATIONAL_DATASET_TLV = 25
    THREAD_DISCOVERY_TLV = 26
    UNKNOWN_TLV = -1

    def __str__(self):
        return self.name

    @classmethod
    def get_by_value(cls, value):
        """
        Get enum by value
        """
        for tlv in cls.__members__.values():
            if tlv.value_TLV == value:
                return tlv
        return cls.UNKNOWN_TLV
