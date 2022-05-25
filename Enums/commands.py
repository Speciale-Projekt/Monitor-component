from enum import Enum


class Commands(Enum):
    """
    Enum of all possible commands types for the package.
    """
    LINK_REQUEST = 0
    LINK_ACCEPT = 1
    LINK_ACCEPT_AND_REQUEST = 2
    LINK_REJECT = 3
    ADVERTISEMENT = 4
    UPDATE = 5
    UPDATE_REQUEST = 6
    DATA_REQUEST = 7
    DATA_RESPONSE = 8
    PARENT_REQUEST = 9
    PARENT_RESPONSE = 10
    CHILD_ID_REQUEST = 11
    CHILD_ID_RESPONSE = 12
    CHILD_UPDATE_REQUEST = 13
    CHILD_UPDATE_RESPONSE = 14
    ANNOUNCE = 15
    DISCOVERY_REQUEST = 16
    DISCOVERY_RESPONSE = 17
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
