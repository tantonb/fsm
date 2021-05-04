import voluptuous as vol


class Transition:
    """Defines an action that transitions state machine from one state to 
    another.
    """

    def __init__(self, action, from_state, to_state):
        self._action = action
        self._from = from_state
        self._to = to_state

    @property
    def action(self):
        return self._action

    @property
    def from_state(self):
        return self._from

    @property
    def to_state(self):
        return self._to
