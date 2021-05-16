"""Fsm
A simple implimentation of a finite state machine that can be associated with a
model object to manage the model's state. 
"""

from functools import partial

from voluptuous import MultipleInvalid
import yaml
from yaml import Loader

from fsm.schema import FSM_SCHEMA, STATE_SCHEMA, TRANSITION_SCHEMA
from fsm.state import State
from fsm.transition import Transition


class FsmError(Exception):
    """Exception type raised by Fsm"""


class Fsm:
    """Implementation of a finite state machine.
    
    Fsm maintains a list of known states.  It associates a state with a
    model object and adds methods to the model to check state and perform 
    state transitions.

    Fsm manages an internal transition table in the form of a mapping 
    of state names to a set of triggering actions, each of which actions
    are mapped to a Transition instance.  The Transition instance encapsulates
    the action, from_state and to_state of a transition allowing state to be
    changed from one to another via an action.
    """

    def __init__(
        self,
        model=None,
        states=None,
        transitions=None,
        start_state=None,
        feedback=True,
    ):
        self._start_state = start_state
        self._model = None
        self._states = {}
        self._transitions = {}
        self._feedback = feedback

        # for now explicit start state is required
        # but might be auto generated in the future
        if start_state is None:
            raise FsmError("No start state provided")

        model = self if model is None else model

        if states:
            self.add_states(states)

        if transitions:
            self.add_transitions(transitions)

        self.set_model(model)

    def set_model(self, model):
        """Associates a model object with this state machine.  
        
        On assignment all existing states and transitions will be associated
        with the model.

        Models must allow attributes to be assigned to allow state, state
        functions and action functions to be set.

        Model state are always initialized to the specified start state.
        """

        # fsm relies on being able to assign new attributes to the model,
        # this makes sure attribute assignment is allowed
        if not hasattr(model, "__dict__"):
            raise ValueError(
                "Invalid model object, does not support dynamic attributes",
            )

        # add state is_* methods to model
        for state in self._states.values():
            self._add_state_check_to_model(model, state.name)

        # add transition methods to model
        for actions in self._transitions.values():
            for tran in actions.values():
                self._add_transition_to_model(model, tran)

        self._model = model
        self._set_state(self._start_state)

    def _is_state(self, model, state_name):
        """Returns true if the model's state matches the state_name.
        Used by state checker functions.
        """
        return getattr(model, "state", None) == state_name

    def _add_state_check_to_model(self, model, state_name):
        """Add state check method to model for the given state"""
        setattr(
            model,
            f"is_{state_name}",
            partial(self._is_state, model, state_name),
        )

    def add_state(self, state):
        """Adds a new state and adds is_<state> function to model."""

        # ensure state has type State (can convert from str name)
        if isinstance(state, str):
            state = State(state)
        elif not isinstance(state, State):
            try:
                state = State(**STATE_SCHEMA(state))
            except MultipleInvalid:
                raise ValueError("Invalid state data", state)

        self._states[state.name] = state

        # model may not be set yet...
        if self._model:
            self._add_state_check_to_model(self._model, state.name)

    def add_states(self, states):
        """Adds states from an iterable"""
        if not isinstance(states, (list, tuple)):
            raise TypeError(f"Invalid states {states}, must be iterable")
        for s in states:
            self.add_state(s)

    def get_state(self):
        """Retrieves the state object representing the current state 
        in the model.
        """
        return self._states[self._model.state]

    def _set_state(self, state_name):
        """Sets the state in the model. Invalid states will raise an 
        FsmError exception.  This can be used to set state without
        triggering call backs (for example when initializing), see 
        _change_state().  Returns new State object.
        """
        if not state_name in self._states:
            raise FsmError("Invalid state", state_name)
        setattr(self._model, "state", state_name)
        return self._states[state_name]

    def _change_state(self, new_state):
        """Changes state from one to another.  This will invoke any
        callbacks associated with the states (on_exit, on_enter) if
        the state is changed.
        """

        # make sure state is actually changing
        cur_state = self.get_state()
        if cur_state.name == new_state:
            return

        # exit/enter callbacks made as state changes
        cur_state.on_exit.call_on(self._model)
        cur_state = self._set_state(new_state)
        cur_state.on_enter.call_on(self._model)

    def _add_transition_to_model(self, model, transition):
        """Add action function to trigger state transition in the model"""
        setattr(
            model, transition.action, partial(self.perform, transition.action)
        )

    def add_transition(self, transition):
        """Adds a transition. The transition parameter may be a Transition 
        object or valid transition data according to the Transition data 
        validator.  
        """
        if not isinstance(transition, Transition):
            try:
                transition = Transition(**TRANSITION_SCHEMA(transition))
            except MultipleInvalid:
                raise ValueError("Invalid transition data", transition)

        # from_state -> actions -> Transition
        actions = self._transitions.get(transition.from_state)
        if actions is None:
            actions = {}
            self._transitions[transition.from_state] = actions
        actions[transition.action] = transition
        if self._model:
            self._add_transition_to_model(self._model, transition)

    def add_transitions(self, transitions):
        """Add multiple transitions from an iterable"""
        if not isinstance(transitions, (list, tuple)):
            raise TypeError(
                f"Invalid transitions {transitions}, must be iterable"
            )
        for t in transitions:
            self.add_transition(t)

    def get_actions(self, state=None):
        """Returns a list of action names for a state if provided, or for
        the current state.
        """
        state = self._model.state if state is None else state
        return list(self._transitions.get(state, {}).keys())

    @property
    def actions(self):
        """Returns list of available actions for the current state"""
        return self.get_actions()

    def perform(self, action):
        """Performs an action to trigger a state transition. Raises FsmError
        if action is not valid for the current state.
        """

        # retrieve actions associated with current state
        from_state = self._model.state
        actions = self._transitions.get(from_state)
        if not actions:
            raise FsmError(f"No actions found for current state '{from_state}'")

        # retrieve transition associated with the action
        transition = actions.get(action)
        if not transition:
            raise FsmError(
                f"Cannot perform action '{action}' in state '{from_state}'"
            )

        # change state
        transition.on_before.call_on(self._model)
        self._change_state(transition.to_state)
        transition.on_after.call_on(self._model)

        # user feedback
        if self._feedback:
            print(
                f"Action '{action}' performed, state transitioned from"
                f" '{transition.from_state}' to '{transition.to_state}'"
            )


def create_fsm(data=None, doc=None, filename=None, **kwargs):
    """Generate state machine using provided initialization data"""

    if filename:
        with open(filename) as fin:
            doc = fin.read()

    # fsm configuration can be encoded in yaml (or json)
    if doc:
        data = yaml.load(doc, Loader=Loader)

    if not data:
        raise ValueError("No data provided for Fsm configuration")

    data = FSM_SCHEMA(data)
    data.update(kwargs)
    return Fsm(**data)
