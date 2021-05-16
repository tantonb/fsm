import pytest

import voluptuous as vol

from fsm import CB_SCHEMA, STATE_SCHEMA, TRANSITION_SCHEMA


def test_cb_schema_valid():
    CB_SCHEMA("cb1")
    CB_SCHEMA(["cb1", "cb2"])


def test_state_schema_valid():
    STATE_SCHEMA("s1")
    STATE_SCHEMA({"name": "s1"})
    STATE_SCHEMA({"name": "s1", "on_enter": "cb1"})
    STATE_SCHEMA({"name": "s1", "on_exit": "cb1"})
    STATE_SCHEMA({"name": "s1", "on_enter": "cb1", "on_exit": "cb2"})


def test_transition_schema_validation_invalid():
    invalids = [
        None,
        "invalid type",
        {"missing": "states"},
        {"action": "action", "missing": "end state"},
    ]

    for data in invalids:
        with pytest.raises(vol.MultipleInvalid):
            TRANSITION_SCHEMA(data)


def test_transition_schema_validation_valid():
    TRANSITION_SCHEMA({"action": "a1", "from_state": "s1", "to_state": "s2"})
    TRANSITION_SCHEMA(
        {
            "action": "a1",
            "from_state": "s1",
            "to_state": "s2",
            "on_before": "cb1",
        }
    )
    TRANSITION_SCHEMA(
        {
            "action": "a1",
            "from_state": "s1",
            "to_state": "s2",
            "on_after": "cb1",
        }
    )
    TRANSITION_SCHEMA(
        {
            "action": "a1",
            "from_state": "s1",
            "to_state": "s2",
            "on_before": "cb1",
            "on_after": "cb2",
        }
    )

