from Enums.commands import Commands
from Statemachine.InvalidStateException import InvalidStateException


class State(object):
    """
    This class holds the state of the statemachine.
    Also what message command has been executed for reaching this state.
    """

    def __init__(self, name: str, command: Commands | None):
        self.name = name
        self.command = command

    def __str__(self):
        return f"name: ({self.name}), command: ({self.command if self.command else None})"


class Rules(object):
    """
    Class for holding the rules for how the states should change based on commands
    """

    def __init__(self):
        self.first_state = None
        self.first_state: State
        self.rest_of_rule: [Rules] = []

    def next_rule(self, rule: Rules) -> Rules:
        """
        Add a rule to the rules list
        :param first_state:
        :param rest_of_rule:
        :return: None
        """
        self.rest_of_rule.append(rule)
        return rule

    def validate(self, state: State, command: Commands):
        """
        Validate the rules
        :param state: State to validate
        :param command: Command to validate
        :return: the next rule if the state and command are valid
        """
        if self.rest_of_rule[0] == state.name and self.first_state.command == command:
            return self.rest_of_rule[0]
        for rule in self.rest_of_rule[1:]:
            if rule.validate(state, command):
                raise InvalidStateException(f"The state received ({state}) obtained with the command ({command}) is "
                                            f"first later in the rulelist")
        return None

    @property
    def next_state(self):
        """
        Get the next state
        :return: the next state
        """
        return self.rest_of_rule[0].first_state


    def __str__(self):
        return f"first_state: {self.first_state}, rest_of_rule: {self.rest_of_rule}"
