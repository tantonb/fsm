import pytest

from fsm import State


def test_state_missing_name():
    with pytest.raises(ValueError):
        State()


def test_state_with_name():
    s = State("s1")
    assert s.name == "s1"
    s = State(name="s1")
    assert s.name == "s1"


def test_state_with_on_enter():
    cb1 = "cb1"
    s = State("s1", on_enter=cb1)
    assert s.on_enter.callbacks == [cb1]


def test_state_with_on_exit():
    cb1 = "cb1"
    s = State("s1", on_exit=cb1)
    assert s.on_exit.callbacks == [cb1]


def test_state_add_on_enter():
    cb1 = "cb1"
    s = State("s1")
    assert s.on_enter.callbacks == []
    s.on_enter.add(cb1)
    assert s.on_enter.callbacks == [cb1]


def test_state_add_on_exit():
    cb1 = "cb1"
    s = State("s1")
    assert s.on_exit.callbacks == []
    s.on_exit.add(cb1)
    assert s.on_exit.callbacks == [cb1]

