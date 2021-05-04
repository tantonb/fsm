import json

import yaml
from yaml import Loader

from fsm.fsm import Fsm
from fsm.schema import FSM_SCHEMA


def from_data(data, model=None):
    """Generate state machine using provided initialization data"""
    data = FSM_SCHEMA(data)
    data["model"] = model
    return Fsm(**data)


def from_json(doc, model=None):
    """Generate state machine from JSON initialization document"""
    return from_data(json.loads(doc), model=model)


def from_json_file(filename, model=None):
    """Generate state machine from JSON initialization file"""
    with open(filename) as fin:
        return from_json(fin.read(), model=model)


def from_yaml(doc, model=None):
    """Generate state machine from YAML initialization document"""
    return from_data(yaml.load(doc, Loader=Loader), model=model)


def from_yaml_file(filename, model=None):
    """Generate state machine from YAML initialization file"""
    with open(filename) as fin:
        return from_yaml(fin.read(), model=model)
