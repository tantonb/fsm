def as_cb_list(data):
    """Validates callback name or names and returns them as a list.  Standalone
    strings are allowed, along with lists or tuples containing only strings.
    None is converted to an empty list."""
    if data is None:
        return []
    if isinstance(data, (list, tuple)):
        for i in data:
            if not isinstance(i, str):
                raise TypeError()
        return list(data)
    if isinstance(data, str):
        return [data]
    raise TypeError()


class CallbackManager:
    """A class to manage a list of named callback functions and call them
    on a target.
    """

    def __init__(self, callbacks=None):
        self._callbacks = as_cb_list(callbacks)

    @property
    def callbacks(self):
        """Returns a copy of the internal callback list"""
        return list(self._callbacks)

    def add(self, callback):
        """Adds callbacks to the internal callback list"""
        self._callbacks += as_cb_list(callback)

    def call_on(self, target):
        """Given a target object looks for callable attributes in the
        callback list.  Each callable found is called.
        """
        for cb in self._callbacks:
            if hasattr(target, cb):
                c = getattr(target, cb)
                if callable(c):
                    c()

