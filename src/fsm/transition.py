import voluptuous as vol


from fsm.util import CallbackManager


class Transition:
    """Defines an action that transitions state machine from one state to 
    another.
    """

    def __init__(
        self, action, from_state, to_state, on_before=None, on_after=None
    ):
        self._action = action
        self._from = from_state
        self._to = to_state
        self._on_before = CallbackManager(on_before)
        self._on_after = CallbackManager(on_after)

    @property
    def action(self):
        return self._action

    @property
    def from_state(self):
        return self._from

    @property
    def to_state(self):
        return self._to

    @property
    def on_before(self):
        return self._on_before

    @property
    def on_after(self):
        return self._on_after
