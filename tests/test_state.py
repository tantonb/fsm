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


def test_state_as_list():
    s = State("s1")
    assert s.as_list([1]) == [1]
    assert s.as_list((1,)) == [1]
    assert s.as_list("str") == ["str"]
    with pytest.raises(TypeError):
        s.as_list(1)


def test_state_with_on_enter():
    cb1 = "cb1"
    s = State("s1", on_enter=cb1)
    assert s.on_enter == [cb1]
    s = State("s1", on_enter=[cb1])
    assert s.on_enter == [cb1]
    s = State("s1", on_enter=(cb1,))
    assert s.on_enter == [cb1]


def test_state_with_on_exit():
    cb1 = "cb1"
    s = State("s1", on_exit=cb1)
    assert s.on_exit == [cb1]
    s = State("s1", on_exit=[cb1])
    assert s.on_exit == [cb1]
    s = State("s1", on_exit=(cb1,))
    assert s.on_exit == [cb1]


def test_state_add_on_enter():
    cb1 = "cb1"
    s = State("s1")
    assert s.on_enter == []
    s.add_on_enter(cb1)
    assert s.on_enter == [cb1]
    cb2 = "cb2"
    cb3 = "cb3"
    cb23 = [cb2, cb3]
    s.add_on_enter(cb23)
    assert s.on_enter == [cb1, cb2, cb3]


def test_state_add_on_exit():
    cb1 = "cb1"
    s = State("s1")
    assert s.on_exit == []
    s.add_on_exit(cb1)
    assert s.on_exit == [cb1]
    cb2 = "cb2"
    cb3 = "cb3"
    cb23 = [cb2, cb3]
    s.add_on_exit(cb23)
    assert s.on_exit == [cb1, cb2, cb3]

