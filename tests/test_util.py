from unittest.mock import MagicMock

import pytest

from fsm.util import as_cb_list, CallbackManager


def test_as_list_with_valids():
    assert as_cb_list(None) == []
    assert as_cb_list(["a"]) == ["a"]
    assert as_cb_list(("a",)) == ["a"]
    assert as_cb_list("str") == ["str"]


def test_as_list_with_invalids():
    invalids = [1, [1], (1,), ["a", 1, "b"]]
    for case in invalids:
        with pytest.raises(TypeError):
            as_cb_list(case)


def test_callback_manager_instantiation():
    cbm = CallbackManager("cb1")
    assert cbm.callbacks == ["cb1"]


def test_callback_manager_add():
    cbm = CallbackManager()
    assert cbm.callbacks == []
    cbm.add("cb1")
    assert cbm.callbacks == ["cb1"]
    cbm.add(["cb2", "cb3"])
    assert cbm.callbacks == ["cb1", "cb2", "cb3"]


def test_callback_manager_call_on():
    class Model:
        pass

    model = Model()
    model.cb1 = MagicMock(name="cb1")
    model.cb2 = MagicMock(name="cb2")
    cbm = CallbackManager(["cb1", "cb2"])
    cbm.call_on(model)
    assert model.cb1.called
    assert model.cb2.called
