from fsm import State


def test_state():
    s = State("name")
    assert s.name == "name"

