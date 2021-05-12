class State:
    """Encapsulates state machine state"""

    def __init__(self, name=None, on_enter=None, on_exit=None):
        if not name:
            raise ValueError("Name parameter required")
        self._name = name
        self._on_enter = []
        if on_enter:
            self.add_on_enter(on_enter)
        self._on_exit = []
        if on_exit:
            self.add_on_exit(on_exit)

    def as_list(self, data):
        if isinstance(data, (list, tuple)):
            return list(data)
        if isinstance(data, str):
            return [data]
        raise TypeError()

    def add_on_enter(self, on_enter):
        self._on_enter += self.as_list(on_enter)

    def add_on_exit(self, on_exit):
        self._on_exit += self.as_list(on_exit)

    @property
    def name(self):
        return self._name

    @property
    def on_enter(self):
        return self._on_enter

    @property
    def on_exit(self):
        return self._on_exit

