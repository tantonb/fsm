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

The class `Fsm` implements a finite state machine that maintains a `state` on a target `model` object and allows `transitions` from one state to another via triggering `actions`.  It is designed to be associated with a separate `model` object, although it can function as a standalone state machine (using itself as the model).  `Fsm` also supports callbacks, which is where things get a little more interesting.  Each `state` may call any number of `on_exit` and `on_enter` callback methods on the model which are triggered as the state changes during transitions.  Similarly, callbacks may be registered on transitions under `on_before` and `on_after` and will trigger when an action is performed that triggers a transition (even if state does not change).  The order of callbacks would be `[on_before]`, `[on_exit]`, `[on_enter]`, `[on_after]`.

### Example

Fsm machines can be instantiated in several ways.  Here's a quick example based on the model class defined in `examples/ex4.py`:

```python
# a class defining a book model with several callback methods
class Book:
    def __init__(self, page_count=3):
        self._page_count = page_count
        self._page_num = 1
        self._is_open = False

    def on_open(self):
        self._is_open = True
        self.show_status()

    def on_close(self):
        self._is_open = False
        self.show_status()

    def on_forward(self):
        if self._page_num < self._page_count:
            self._page_num += 1
        else:
            print("Already on last page.")
        self.show_status()

    def on_back(self):
        if self._page_num > 1:
            self._page_num -= 1
        else:
            print("Already on first page.")
        self.show_status()

    def show_status(self):
        if self._is_open:
            print("The book is open to page", self._page_num)
        else:
            print("The book is closed.")
```
This class defines a number of callbacks that can be registered with states and transitions in a state machine:

```bash
>>> # fsm can load from yaml or json docs or files containing them
>>> from fsm import create_fsm
>>> from ex4 import Book
>>> book = Book()
>>> fsm = create_fsm(
...     doc="""
...         # a book with callbacks
...         start_state: closed
... 
...         states: 
...             - name: closed
...               on_enter: on_close
... 
...             - name: opened
...               on_enter: on_open
... 
... 
...         transitions:
... 
...             - action:       open
...               from_state:   closed
...               to_state:     opened
... 
...             - action:       forward
...               from_state:   opened
...               to_state:     opened
...               on_before:    on_forward
... 
...             - action:       back
...               from_state:   opened
...               to_state:     opened
...               on_before:    on_back
... 
...             - action:       close
...               from_state:   opened
...               to_state:     closed
...         """,
...     model=book,
...     feedback=False,
... )
>>> # now we have a machine associated with our book model
>>> # we've also disabled default user feedback
>>> book.state
'closed'
>>> # state flags have been generated on the model
>>> book.is_closed()
True
>>> # the state machine can tell us current available actions
>>> fsm.get_actions()
['open']
>>> # open() will trigger on_open() in the model
>>> book.is_opened()
False
>>> book.open()
The book is open to page 1
>>> book.is_opened()
True
>>> fsm.get_actions()
['forward', 'back', 'close']
>>> # calling forward and back will trigger the transition callbacks
>>> book.forward()
The book is open to page 2
>>> book.forward()
The book is open to page 3
>>> book.back()
The book is open to page 2
>>> book.close()
The book is closed.
>>> # invalid actions will raise FsmError
>>> book.back()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/tyler/projects/fsm/src/fsm/fsm.py", line 228, in perform
    raise FsmError(
fsm.fsm.FsmError: Cannot perform action 'back' in state 'closed'
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
