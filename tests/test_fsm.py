"""Test kincode.fsm"""
from unittest import mock

import pytest
import voluptuous as vol
import yaml

from fsm import (
    create_fsm,
    Fsm,
    FsmError,
)


@pytest.fixture(name="fsm_doc")
def fixture_fsm_doc():
    return """
        start_state: s1
        states:
            - s1
            - name: s2
              on_enter: on_callback
        transitions:
            - action: a1
              from_state: s1
              to_state: s2
            - action: a2
              from_state: s1
              to_state: s1
    """


@pytest.fixture(name="fsm_data")
def fixture_fsm_data(fsm_doc):
    return yaml.load(fsm_doc, Loader=yaml.Loader)


class DummyModel:
    def __init__(self):
        self.cb_count = 0

    def on_callback(self):
        self.cb_count += 1


@pytest.fixture(name="model")
def fixture_model():
    return DummyModel()


def test_create_no_states_start_state():
    with pytest.raises(FsmError):
        Fsm()


def test_create_no_start_state():
    with pytest.raises(FsmError):
        Fsm(states=["s1"])


def test_create_invalid_start_state():
    with pytest.raises(FsmError):
        Fsm(states=["s1"], start_state="s2")


def test_create_invalid_states_non_iterable():
    with pytest.raises(TypeError):
        Fsm(states="s1", start_state="s1")


def test_create_invalid_states_type():
    with pytest.raises(ValueError):
        Fsm(states=[1], start_state="x")


def test_create_valid_states_only():
    fsm = Fsm(states=["s1"], start_state="s1")
    assert fsm.state == "s1"  # pylint: disable=maybe-no-member


def test_create_invalid_transitions_non_iterable():
    with pytest.raises(TypeError):
        Fsm(states=["s1"], transitions="invalid", start_state="s1")


def test_create_invalid_transitions_data():
    transitions = [{"action": "invalid"}]
    with pytest.raises(ValueError):
        Fsm(states=["s1"], start_state="s1", transitions=transitions)


def test_create_invalid_model_object():
    with pytest.raises(ValueError):
        Fsm(model=object(), states=["s1"], start_state="s1")


def test_create_valid_model_object(model):
    assert not hasattr(model, "state")
    Fsm(model=model, states=["s1"], start_state="s1")
    assert model.state == "s1"


def test_is_state():
    fsm = Fsm(states=["s1", "s2"], start_state="s1")
    assert hasattr(fsm, "is_s1") and getattr(fsm, "is_s1")()
    assert hasattr(fsm, "is_s2") and not getattr(fsm, "is_s2")()


def test_transition_success(model):
    fsm = Fsm(
        model=model,
        states=["s1", "s2"],
        transitions=[{"action": "a1", "from_state": "s1", "to_state": "s2"}],
        start_state="s1",
    )
    assert model.state == "s1"
    fsm.perform("a1")
    assert model.state == "s2"


def test_transition_fail_invalid_action(model):
    fsm = Fsm(
        model=model,
        states=["s1", "s2"],
        transitions=[{"action": "a1", "from_state": "s1", "to_state": "s2"}],
        start_state="s1",
    )
    assert model.state == "s1"
    with pytest.raises(FsmError):
        fsm.perform("invalid")


def test_transition_with_action_function_on_model(model):
    Fsm(
        model=model,
        states=["s1", "s2"],
        transitions=[{"action": "a1", "from_state": "s1", "to_state": "s2"}],
        start_state="s1",
    )
    assert model.state == "s1"
    model.a1()
    assert model.state == "s2"


def test_actions_property(fsm_data):
    fsm = create_fsm(data=fsm_data)
    assert fsm.actions == ["a1", "a2"]


def test_add_state_after_create(model):
    fsm = Fsm(
        model=model,
        states=["s1", "s2"],
        transitions=[{"action": "a1", "from_state": "s1", "to_state": "s2"}],
        start_state="s1",
    )
    fsm.add_state("s3")


def test_add_transition(model):
    fsm = Fsm(
        model=model,
        states=["s1", "s2"],
        transitions=[{"action": "a1", "from_state": "s1", "to_state": "s2"}],
        start_state="s1",
    )
    fsm.add_transition({"action": "a2", "from_state": "s2", "to_state": "s1"})
    assert fsm.get_actions(state="s2") == ["a2"]


def test_no_actions_for_state(model):
    fsm = Fsm(
        model=model,
        states=["s1", "s2"],
        transitions=[{"action": "a1", "from_state": "s2", "to_state": "s1"}],
        start_state="s1",
    )
    with pytest.raises(FsmError):
        fsm.perform("a1")


def test_get_valid_action_no_actions():
    fsm = Fsm(
        states=["s1", "s2"],
        transitions=[{"action": "a1", "from_state": "s2", "to_state": "s2"}],
        start_state="s1",
    )
    assert fsm.get_actions(state="s1") == []


def test_create_fsm_from_data(fsm_data, model):
    fsm = create_fsm(model=model, data=fsm_data)
    assert isinstance(fsm, Fsm)
    assert model.state == "s1"  # pylint: disable=maybe-no-member
    assert model.cb_count == 0
    model.a1()  # pylint: disable=maybe-no-member
    assert model.cb_count == 1


def test_create_fsm_from_doc(fsm_doc, model):
    fsm = create_fsm(model=model, doc=fsm_doc)
    assert isinstance(fsm, Fsm)
    assert model.state == "s1"  # pylint: disable=maybe-no-member
    assert model.cb_count == 0
    model.a1()  # pylint: disable=maybe-no-member
    assert model.cb_count == 1


def test_create_fsm_from_file(fsm_doc, model):
    mock_open = mock.mock_open(read_data=fsm_doc)
    with mock.patch("builtins.open", mock_open):
        fsm = create_fsm(model=model, filename="mock_filename")
        assert isinstance(fsm, Fsm)
        assert model.state == "s1"  # pylint: disable=maybe-no-member
        assert model.cb_count == 0
        model.a1()  # pylint: disable=maybe-no-member
        assert model.cb_count == 1


def test_create_fsm_from_json(model):
    doc = """
        {
            "start_state": "s1",
            "states": [
                "s1",
                {
                    "name": "s2",
                    "on_enter": "on_callback"
                }
            ],
            "transitions": [
                {
                    "action": "a1",
                    "from_state": "s1",
                    "to_state": "s2"
                }
            ]
        }
    """
    fsm = create_fsm(model=model, doc=doc)
    assert isinstance(fsm, Fsm)
    # pylint: disable=maybe-no-member
    assert model.state == "s1"
    assert model.cb_count == 0
    model.a1()
    assert model.cb_count == 1


def test_create_fsm_no_data():
    with pytest.raises(ValueError):
        create_fsm()


def test_transition_with_no_state_change(fsm_doc):
    # pylint: disable=maybe-no-member
    fsm = create_fsm(doc=fsm_doc)
    assert fsm.state == "s1"
    fsm.a2()
    assert fsm.state == "s1"
