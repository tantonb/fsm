import pytest

import voluptuous as vol

from fsm import TRANSITION_SCHEMA


def test_transition_schema_validation_invalid():
    invalids = [
        None,
        "invalid type",
        {"missing": "states"},
        {"action": "action", "missing": "end state"},
    ]

    # check invalid transition data
    for data in invalids:
        with pytest.raises(vol.MultipleInvalid):
            TRANSITION_SCHEMA(data)


def test_transition_schema_validation_valid():
    valid = {"action": "a1", "from_state": "s1", "to_state": "s2"}
    expected = valid
    valid = TRANSITION_SCHEMA(valid)
    assert expected == valid

