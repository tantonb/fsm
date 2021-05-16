from fsm.util import CallbackManager


class State:
    """Encapsulates state machine state"""

    def __init__(self, name=None, on_enter=None, on_exit=None):
        if not name:
            raise ValueError("Name parameter required")
        self._name = name
        self._on_enter = CallbackManager(on_enter)
        self._on_exit = CallbackManager(on_exit)

    @property
    def name(self):
        return self._name

    @property
    def on_enter(self):
        return self._on_enter

    @property
    def on_exit(self):
        return self._on_exit

