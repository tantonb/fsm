from fsm import Transition


def test_transition():
    t = Transition("action", "from", "to")
    assert t.action == "action"
    assert t.from_state == "from"
    assert t.to_state == "to"

