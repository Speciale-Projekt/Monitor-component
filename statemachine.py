import commands
from tlvs import TLVS
from commands import Commands

class Thread:
    states = ["Idle", "Processing_Discover", "Processing_Parent_Request", "Processing_ChildID_Request"]
    events = {
        Commands.DISCOVERY_REQUEST: "Processing_Discover",
        Commands.DISCOVERY_RESPONSE: "Idle",
        Commands.PARENT_REQUEST: "Processing_Parent_Request",
        Commands.PARENT_RESPONSE: "Idle",
        Commands.CHILD_ID_REQUEST: "Processing_ChildID_Request",
        Commands.CHILD_ID_RESPONSE: "Idle"
    }


class ThreadTransition:
    def __init__(self, from_state, event, to_state):
        self.from_state = from_state
        self.event = event
        self.to_state = to_state


def get_command_type(content) -> Commands:
    if content[0] == 255:
        command_type = Commands.get_by_value(content[1])
    elif content[0] == 0:
        command_type = Commands.get_by_value(content[11])
    else:
        command_type = Commands.UNKNOWN

    if command_type.value >= 0:
        return command_type


class ThreadStateMachine:
    def __init__(self, curr_state):
        self.curr_state = curr_state
        self.transitions = []

    def event_handler(self, event):
        self.transitions.append(ThreadTransition(self.curr_state, event, Thread.events.get(event)))

    def advance_state(self, content):
        commandtype = get_command_type(content)
        self.transitions.append(ThreadTransition(self.curr_state, commandtype, Thread.events.get(commandtype)))

    def to_str(self):
        output = "",
        for transition in self.transitions:
            t = ThreadTransition(transition)
            output = output + " --" + t.event + "--> " "("+t.to_state+")"

        return output
