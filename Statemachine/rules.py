import abc

from Enums.commands import Commands
from Enums.tlvs import TLVS


class ContainedTLVS:
    def __init__(self, optional_tlvs: list[TLVS] = None, mandatory_tlvs: list[TLVS] = None):
        if mandatory_tlvs is None:
            mandatory_tlvs = []
        if optional_tlvs is None:
            optional_tlvs = []
        self.optional_tlvs = optional_tlvs
        self.mandatory_tlvs = mandatory_tlvs

    def validate(self, tlvs: list[TLVS]) -> bool:
        """
        Checks if all mandatory TLV's are present, and that there are no TLVs not present in either the mandatory or
        optional list.
        :param tlvs: The tlvs to check on.
        :return: bool for if the tlvs are valid.
        """

        if len(tlvs) == 0 and (len(self.mandatory_tlvs) > 0 or len(self.optional_tlvs) > 0) \
                or len(tlvs) != len(self.mandatory_tlvs) + len(self.optional_tlvs):
            return False
        for tlv in self.mandatory_tlvs:
            if tlv not in tlvs:
                return False

        for tlv in tlvs:
            if tlv not in self.mandatory_tlvs and tlv not in self.optional_tlvs:
                return False

        return True

    def __dict__(self):
        return {
            'optional_tlvs': self.optional_tlvs,
            'mandatory_tlvs': self.mandatory_tlvs
        }

    def __str__(self):
        return "ContainedTLVS(optional_tlvs={}, mandatory_tlvs={})".format(self.optional_tlvs, self.mandatory_tlvs)


message_commands_succession = {
    Commands.DISCOVERY_REQUEST: {
        "TLVS": ContainedTLVS(mandatory_tlvs=[TLVS.THREAD_DISCOVERY_TLV]),
        "succession": {
            Commands.DISCOVERY_RESPONSE: ContainedTLVS(mandatory_tlvs=[TLVS.THREAD_DISCOVERY_TLV])
        }
    },

    Commands.LINK_REQUEST: {
        "TLVS": ContainedTLVS(mandatory_tlvs=[TLVS.SOURCE_ADDRESS_TLV, TLVS.LEADER_DATA_TLV, TLVS.CHALLENGE_TLV,
                                              TLVS.VERSION_TLV, TLVS.TLV_REQUEST_TLV]),
        "succession": {
            Commands.LINK_ACCEPT: ContainedTLVS(optional_tlvs=[TLVS.MLE_FRAME_COUNTER_TLV, TLVS.CHALLENGE_TLV],
                                                mandatory_tlvs=[TLVS.SOURCE_ADDRESS_TLV, TLVS.LEADER_DATA_TLV,
                                                                TLVS.RESPONSE_TLV, TLVS.VERSION_TLV,
                                                                TLVS.LINK_LAYER_FRAME_COUNTER_TLV,
                                                                TLVS.LINK_MARGIN_TLV]),
            Commands.LINK_REJECT: ContainedTLVS(mandatory_tlvs=[TLVS.STATUS_TLV]),
            Commands.LINK_ACCEPT_AND_REQUEST: ContainedTLVS(
                optional_tlvs=[TLVS.MLE_FRAME_COUNTER_TLV, TLVS.CHALLENGE_TLV, TLVS.TLV_REQUEST_TLV],
                mandatory_tlvs=[TLVS.SOURCE_ADDRESS_TLV, TLVS.LEADER_DATA_TLV, TLVS.RESPONSE_TLV, TLVS.VERSION_TLV,
                                TLVS.LINK_LAYER_FRAME_COUNTER_TLV, TLVS.LINK_MARGIN_TLV]),
        }

    },

    Commands.PARENT_REQUEST: {
        "TLVS": ContainedTLVS(mandatory_tlvs=[TLVS.MODE_TLV, TLVS.CHANNEL_TLV, TLVS.SCAN_MASK_TLV, TLVS.VERSION_TLV]),
        "succession": {
            Commands.PARENT_RESPONSE: ContainedTLVS(optional_tlvs=[TLVS.MLE_FRAME_COUNTER_TLV],
                                                    mandatory_tlvs=[TLVS.SOURCE_ADDRESS_TLV, TLVS.CHALLENGE_TLV,
                                                                    TLVS.RESPONSE_TLV,
                                                                    TLVS.LINK_LAYER_FRAME_COUNTER_TLV,
                                                                    TLVS.LEADER_DATA_TLV, TLVS.CONNECTIVITY_TLV,
                                                                    TLVS.LINK_MARGIN_TLV, TLVS.VERSION_TLV]),
        }
    },
    Commands.CHILD_ID_REQUEST: {
        "TLVS": ContainedTLVS(optional_tlvs=[TLVS.MLE_FRAME_COUNTER_TLV, TLVS.RESPONSE_TLV, TLVS.ACTIVE_TIMESTAMP_TLV,
                                             TLVS.PENDING_TIMESTAMP_TLV],
                              mandatory_tlvs=[TLVS.MODE_TLV, TLVS.TIMEOUT_TLV, TLVS.RESPONSE_TLV,
                                              TLVS.LINK_LAYER_FRAME_COUNTER_TLV, TLVS.VERSION_TLV]),
        "succession": {
            Commands.CHILD_ID_RESPONSE: ContainedTLVS(
                optional_tlvs=[TLVS.ROUTE64_TLV, TLVS.NETWORK_DATA_TLV, TLVS.ADDRESS_REGISTRATION_TLV,
                               TLVS.ACTIVE_TIMESTAMP_TLV, TLVS.PENDING_TIMESTAMP_TLV,
                               TLVS.ACTIVE_OPERATIONAL_DATASET_TLV, TLVS.PENDING_OPERATIONAL_DATASET_TLV],
                mandatory_tlvs=[TLVS.ADDRESS16_TLV, TLVS.LEADER_DATA_TLV, TLVS.SOURCE_ADDRESS_TLV, ])
        }
    }

}


class Message:
    command: Commands
    tlvs: list[TLVS]

    def __str__(self):
        return "Message(command={}, tlvs={})".format(self.command, self.tlvs)


def valid_order_for_messages(previous_message: Message, this_message: Message) -> (bool, str | None):
    """
    Derives the previous message in message_commands_succession,
    then it returns a bool if the previous message is the correct one
    :param previous_message: previous message
    :param this_message: current message
    :return: bool if the message order is correct, str bonus informatio as to why it is not
    """
    if this_message is None:
        raise ValueError("Value cannot be None")

    if this_message.command in message_commands_succession \
            and message_commands_succession[this_message.command].get("TLVS").validate(this_message.tlvs):
        return True

    if previous_message is None:
        raise ValueError("Previous message cannot be None when this_message is not the first message")

    # Check if this_message is the successor of the previous_message
    if previous_message.command in message_commands_succession \
            and message_commands_succession[previous_message.command].get("succession").get(this_message.command):
        # Check if TLVs are valid
        if message_commands_succession[previous_message.command].get("succession").get(this_message.command).validate(
                this_message.tlvs) and message_commands_succession[previous_message.command].get("TLVS").validate(
            previous_message.tlvs):
            return True
        else:
            return False, "Commands are valid, but TLVs are not valid"
    return False, "Commands are not valid"
