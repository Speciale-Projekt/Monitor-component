from Enums.commands import Commands


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
    def __init__(self, from_state: str, event: str, to_state: str):
        self.from_state = from_state
        self.event = event
        self.to_state = to_state


class ThreadStateMachine:
    def __init__(self, curr_state):
        self.curr_state = curr_state
        self.transitions = []

    def advance_state(self, cmd_type):
        self.transitions.append(ThreadTransition(self.curr_state, cmd_type, Thread.events.get(cmd_type)))

    def to_str(self):
        output = ""
        for transition in self.transitions:
            transition: ThreadTransition
            output = output + " --" + transition.event.__str__() + "--> " "(" + transition.to_state + ")"

        return output
