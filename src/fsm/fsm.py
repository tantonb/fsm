"""Finite state machine
A simple implimentation of a finite state machine that can be associated with a
model object to manage the model's state.  Defines State and Transition classes
used by the finite state machine class Fsm.
"""

from functools import partial

from voluptuous import MultipleInvalid

from fsm.schema import TRANSITION_SCHEMA
from fsm.state import State
from fsm.transition import Transition


class FsmError(Exception):
    """Exception type raised by a finite state machine"""


class Fsm:
    """Implementation of a finite state machine"""

    def __init__(
        self, model=None, states=None, transitions=None, start_state=None
    ):
        self._model = None
        self._states = {}
        self._transitions = {}

        if start_state is None:
            raise FsmError("No start state provided")
        model = self if model is None else model
        if states:
            self.add_states(states)
        if transitions:
            self.add_transitions(transitions)
        self.set_model(model, start_state)

    def set_model(self, model, start_state):
        """Associates a model object with this state machine.  Models must allow
        attributes to be assigned to allow state, state functions and action 
        functions to be set.
        """
        if not hasattr(model, "__dict__"):
            raise ValueError(
                "Invalid model object, does not support dynamic attributes",
            )
        for state in self._states.values():
            self._add_state_to_model(model, state.name)
        for actions in self._transitions.values():
            for tran in actions.values():
                self._add_transition_to_model(model, tran)
        self._model = model
        self.set_state(start_state)

    def _is_state(self, model, state_name):
        """Returns true if the model's state matches the state_name"""
        return getattr(model, "state", None) == state_name

    def _add_state_to_model(self, model, state_name):
        """Add state check function to model for the given state"""
        func_name = f"is_{state_name}"
        func = partial(self._is_state, model, state_name)
        setattr(model, func_name, func)

    def add_state(self, state):
        """Add a new state.  Add state check function to model if model is present"""
        if isinstance(state, str):
            state = State(state)
        elif not isinstance(state, State):
            raise TypeError(
                f"Invalid state data '{state}   ', must be str or State object"
            )

        self._states[state.name] = state
        if self._model:
            self._add_state_to_model(self._model, state.name)

    def add_states(self, states):
        """Adds multiple states from an iterable"""
        if not isinstance(states, (list, tuple)):
            raise TypeError("Invalid states, must be iterable")
        for s in states:
            self.add_state(s)

    def set_state(self, name):
        """Changes the machine state, sets the state in the model"""
        if not name in self._states:
            raise FsmError("Invalid state", name)
        setattr(self._model, "state", name)

    def _add_transition_to_model(self, model, tran):
        """Add action function to trigger state transition in the model"""
        func_name = tran.action
        func = partial(self.perform, tran.action)
        setattr(model, func_name, func)

    def add_transition(self, tran):
        """Adds a transition.  Maps transition's from state to actions mapped
        to allowed transitions.  The tran parameter may be a Transition object
        or valid transition data according to the Transition data validator.
        """
        if not isinstance(tran, Transition):
            try:
                tran = TRANSITION_SCHEMA(tran)
                tran = Transition(**tran)
            except MultipleInvalid:
                raise ValueError("Invalid transition data", tran)

        actions = self._transitions.get(tran.from_state)
        if actions is None:
            actions = {}
            self._transitions[tran.from_state] = actions
        actions[tran.action] = tran
        if self._model:
            self._add_transition_to_model(self._model, tran)

    def add_transitions(self, transitions):
        """Add multiple transitions from an iterable"""
        for t in transitions:
            self.add_transition(t)

    def get_state_actions(self, state=None):
        """Return a list of action names for the given state.  If state
        is not specified, use the current state
        """
        state = self._model.state if state is None else state
        return list(self._transitions.get(state, {}).keys())

    def perform(self, action):
        """Tries to perform an action to trigger a state transition.
        Raises FsmError if action is not valid for the current state.
        """
        from_state_name = self._model.state
        actions = self._transitions.get(from_state_name)
        if not actions:
            raise FsmError(
                f"No actions found for current state '{from_state_name}'"
            )
        tran = actions.get(action)
        if not tran:
            raise FsmError(
                f"Cannot perform action '{action}' in state '{from_state_name}'"
            )
        print(
            f"Performed action '{action}', state changed from '{tran.from_state}' to '{tran.to_state}'"
        )
        self.set_state(tran.to_state)

    def get_state(self):
        """Fetches the current state from the model"""
        return self._model.state
