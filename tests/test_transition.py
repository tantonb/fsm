from fsm import Transition


def test_transition_instantiation():
    t = Transition("action", "from", "to")
    assert t.action == "action"
    assert t.from_state == "from"
    assert t.to_state == "to"


def test_transition_instantiation_some_more():
    t = Transition(action="action", from_state="from", to_state="to")
    assert t.action == "action"
    assert t.from_state == "from"
    assert t.to_state == "to"


def test_transition_with_on_before():
    t = Transition("action", "from", "to", on_before="before")
    assert t.on_before.callbacks == ["before"]


def test_transition_with_on_after():
    t = Transition("action", "from", "to", on_after="after")
    assert t.on_after.callbacks == ["after"]


def test_transition_add_on_before():
    cb1 = "cb1"
    t = Transition("action", "from", "to")
    assert t.on_before.callbacks == []
    t.on_before.add(cb1)
    assert t.on_before.callbacks == [cb1]


def test_state_add_on_exit():
    cb1 = "cb1"
    t = Transition("action", "from", "to")
    assert t.on_after.callbacks == []
    t.on_after.add(cb1)
    assert t.on_after.callbacks == [cb1]

