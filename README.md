# fsm: Finite State Machine implementation

An implementation of a finite state machine in python.

## Installation

Download the source code from git:

```bash
$ git clone https://github.com/tantonb/fsm.git
```

You'll want to setup a virtual environment and activate it using your preferred method.  Once activated, use pip to install several dependencies.  This will also install the project itself which allows unit tests to import project modules.

```bash
$ cd fsm
$ pip install -r requirements.txt
```

## Usage

The class `Fsm` implements a finite state machine that maintains a `state` on a target `model` object and allows `transitions` from one state to another via triggering `actions`.  It is designed to be associated with a separate `model` object, although it function just as well as a standalone state machine (using itself as the model).

### Example

Fsm machines can be instantiated in several ways.  Here's a quick example using the REPL:

```python
>>> from fsm import from_yaml
>>> # fsm can load configuration from yaml or json documents
>>> # and also from files containing docs
>>> fsm = from_yaml("""
... # a book
... start_state: closed
... 
... states: [closed, page1, page2]
... 
... transitions:
... 
...     - action:       open
...       from_state:   closed
...       to_state:     page1
... 
...     - action:       forward
...       from_state:   page1
...       to_state:     page2
... 
...     - action:       back
...       from_state:   page2
...       to_state:     page1
... 
...     - action:       close
...       from_state:   page1
...       to_state:     closed
... 
...     - action:       close
...       from_state:   page2
...       to_state:     closed
... """
... )
>>> # fsm here is in standalone mode, no associated model
>>> # so state machine is self-contained
>>> fsm.get_state()
'closed'
>>> fsm.state
'closed'
>>> fsm.is_closed()
True
>>> fsm.get_actions()
['open']
>>> fsm.perform("open")
Action 'open' performed, state transitioned from 'closed' to 'page1'
>>> fsm.is_page1()
True
>>> fsm.is_closed()
False
>>> fsm.get_actions()
['forward', 'close']
>>> fsm.forward()
Action 'forward' performed, state transitioned from 'page1' to 'page2'
>>> fsm.get_actions()
['back', 'close']
>>> fsm.close()
Action 'close' performed, state transitioned from 'page2' to 'closed'
>>> fsm.is_closed()
True
>>> # a model can be associated with the fsm at any time
>>> class Book: pass
...
>>> book = Book()
>>> fsm.set_model(book)
>>> # now the model contains state and functionality
>>> book.state
'closed'
>>> fsm.get_actions()
['open']
>>> book.is_closed()
True
>>> book.open()
Action 'open' performed, state transitioned from 'closed' to 'page1'
>>> book.state
'page1'
>>> fsm.get_state()
'page1'
```

## Testing

Unit tests and coverage reporting are provided.

### Test coverage
Test coverage can be determined using the `pytest-cov` pytest coverage plugin.  From the top-level fsm/ directory use 'pytest' to run:

```bash
$ pytest --cov=fsm
```

Test coverage reports can also be generated.  Here reports are generated in html form which can be viewed at `fsm/htmlcov/index.html`:

```bash
$ pytest --cov=fsm --cov-report html
```

## License

[Apache 2.0](https://choosealicense.com/licenses/apache-2.0/)
