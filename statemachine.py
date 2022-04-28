class Thread:
    states = ["Idle", "Processing_Discover", "Processing_Parent_Request", "Processing_ChildID_Request"]
    events = {
        "Discover_Request": "Processing_Discover",
        "Discover_Response": "Idle",
        "Parent_Request": "Processing_Parent_Request",
        "Parent_Response": "Idle",
        "Child_ID_Request": "Processing_ChildID_Request",
        "Child_ID_Response": "Idle"
    }
    command_types = {
        0: "Link_Request",
        1: "Link_Accept",
        2: "Link_Accept_and_Request",
        3: "Link_Reject",
        4: "Advertisement",
        5: "Update",
        6: "Update_Request",
        7: "Data_Request",
        8: "Data_Response",
        9: "Parent_Request",
        10: "Parent_Response",
        11: "Child_ID_Request",
        12: "Child_ID_Response",
        13: "Child_Update_Request",
        14: "Child_Update_Response",
        15: "Announce",
        16: "Discovery_Request",
        17: "Discovery_Response",
    }


class ThreadTransition:
    def __init__(self, from_state, event, to_state):
        self.from_state = from_state
        self.event = event
        self.to_state = to_state


def get_command_type(content):
    if content[0] == 255:
        type = content[1]
    elif content[0] == 0:
        type = content[11]
    else:
        type = -1

    if type >= 0:
        return Thread.command_types.get(type)


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
