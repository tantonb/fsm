doc = """
# a simple book
start_state: closed

states: [closed, page1, page2]

transitions:

    - action:       open
      from_state:   closed
      to_state:     page1

    - action:       forward
      from_state:   page1
      to_state:     page2

    - action:       back
      from_state:   page2
      to_state:     page1

    - action:       close
      from_state:   page1
      to_state:     closed

    - action:       close
      from_state:   page2
      to_state:     closed
"""
