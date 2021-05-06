# fsm: Finite State Machine implementation

An implementation of a finite state machine in python.

## Installation

Download the source code from git:

```bash
git clone https://github.com/tantonb/fsm.git
```

You'll want to setup a virtual environment and activate it using your preferred method.  Once activated, use pip to install several dependencies.  This will also install the project itself which allows unit tests to import project modules.

```bash
cd fsm
pip install -r requirements.txt
```

## Usage

The class `Fsm` implements a finite state machine that maintains a `state` on a target `model` object and allows `transitions` from one state to another via triggering `actions`.  It is designed to be associated with a separate `model` object, although it function just as well as a standalone state machine (using itself as the model).

`(WIP)`

## Testing

Unit tests and coverage reporting are provided.

### Test coverage
Test coverage can be determined using the `pytest-cov` pytest coverage plugin.  From the top-level fsm/ directory use 'pytest' to run:

```bash
$ pytest --cov=fsm
======================================== test session starts ========================================
platform linux -- Python 3.9.2, pytest-6.2.3, py-1.10.0, pluggy-0.13.1
rootdir: /home/tyler/projects/fsm
plugins: cov-2.11.1
collected 27 items                                                                                  

tests/test_fsm.py ..................                                                          [ 66%]
tests/test_schema.py ..                                                                       [ 74%]
tests/test_state.py .                                                                         [ 77%]
tests/test_transition.py .                                                                    [ 81%]
tests/test_util.py .....                                                                      [100%]

----------- coverage: platform linux, python 3.9.2-final-0 -----------
Name                    Stmts   Miss  Cover
-------------------------------------------
src/fsm/__init__.py         9      0   100%
src/fsm/fsm.py             84      0   100%
src/fsm/schema.py           4      0   100%
src/fsm/state.py            6      0   100%
src/fsm/transition.py      15      0   100%
src/fsm/util.py            19      0   100%
-------------------------------------------
TOTAL                     137      0   100%


======================================== 27 passed in 0.17s =========================================
```

Test coverage reports can also be generated.  Here reports are generated in html form which can be viewed at `fsm/htmlcov/index.html`:

```bash
$ pytest --cov=fsm --cov-report html
======================================== test session starts ========================================
platform linux -- Python 3.9.2, pytest-6.2.3, py-1.10.0, pluggy-0.13.1
rootdir: /home/tyler/projects/fsm
plugins: cov-2.11.1
collected 27 items                                                                                  

tests/test_fsm.py ..................                                                          [ 66%]
tests/test_schema.py ..                                                                       [ 74%]
tests/test_state.py .                                                                         [ 77%]
tests/test_transition.py .                                                                    [ 81%]
tests/test_util.py .....                                                                      [100%]

----------- coverage: platform linux, python 3.9.2-final-0 -----------
Coverage HTML written to dir htmlcov


======================================== 27 passed in 0.18s =========================================
```

## License

[Apache 2.0](https://choosealicense.com/licenses/apache-2.0/)
