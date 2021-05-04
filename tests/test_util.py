import json
from unittest import mock

import pytest
import yaml
from yaml import Loader

from fsm import (
    from_data,
    from_json,
    from_json_file,
    from_yaml,
    from_yaml_file,
)


@pytest.fixture(name="json_doc")
def fixture_json_doc():
    return """
    {
        "start_state": "green",
        "states": [
            "green",
            "yellow",
            "red"
        ],
        "transitions": [
            {
                "action": "turn_yellow",
                "from_state": "green",
                "to_state": "yellow"
            },
            {
                "action": "turn_red",
                "from_state": "yellow",
                "to_state": "red"
            },
            {
                "action": "turn_green",
                "from_state": "red",
                "to_state": "green"
            }
        ]
    }
    """


@pytest.fixture(name="yaml_doc")
def fixture_yaml_doc():
    return """
        start_state: green
        
        states: [ green, yellow, red ]

        transitions:

            - action:       yellow
              from_state:   green
              to_state:     yellow

            - action:       red
              from_state:   yellow
              to_state:     red

            - action:       green
              from_state:   red
              to_state:     green
    """


@pytest.fixture(name="json_data")
def fixture_json_data(json_doc):
    return json.loads(json_doc)


@pytest.fixture(name="yaml_data")
def fixture_yaml_data(yaml_doc):
    return yaml.load(yaml_doc, Loader=Loader)


def test_from_data(json_data):
    data = {
        "start_state": "start",
        "states": ["start", "finish"],
        "transitions": [
            {"action": "finish", "from_state": "start", "to_state": "finish"}
        ],
    }
    fsm = from_data(data)
    assert fsm.get_state() == "start"


def test_from_json(json_doc):
    fsm = from_json(json_doc)
    assert fsm.get_state() == "green"


def test_from_json_file(json_doc):
    mock_open = mock.mock_open(read_data=json_doc)
    with mock.patch("builtins.open", mock_open):
        fsm = from_json_file("mock-filename")
        assert fsm.get_state() == "green"


def test_from_yaml(yaml_doc):
    fsm = from_yaml(yaml_doc)
    assert fsm.get_state() == "green"


def test_from_yaml_file(yaml_doc):
    mock_open = mock.mock_open(read_data=yaml_doc)
    with mock.patch("builtins.open", mock_open):
        fsm = from_yaml_file("mock-filename")
        assert fsm.get_state() == "green"
