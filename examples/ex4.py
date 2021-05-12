from fsm import create_fsm, Fsm


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

    def show_status(self):
        if self._is_open:
            print("The book is open to page", self._page_num)
        else:
            print("The book is closed.")


book = Book()
fsm = create_fsm(
    doc="""
# a book with callbacks
start_state: closed

states: 
    - name: closed
      on_enter: on_close

    - name: opened
      on_enter: on_open


transitions:

    - action:       open
      from_state:   closed
      to_state:     opened

    - action:       forward
      from_state:   opened
      to_state:     opened

    - action:       back
      from_state:   opened
      to_state:     opened

    - action:       close
      from_state:   opened
      to_state:     closed
""",
    model=book,
)

