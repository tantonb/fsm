import voluptuous as vol

# validation schema for State object initialization data
STATE_SCHEMA = vol.Schema(str)

# validation schema for Transition object initialization data
TRANSITION_SCHEMA = vol.Schema(
    {
        vol.Required("action"): str,
        vol.Required("from_state"): str,
        vol.Required("to_state"): str,
    }
)

# validation schema for finite state machine (Fsm) initialization data
FSM_SCHEMA = vol.Schema(
    {
        vol.Required("start_state"): str,
        vol.Required("states"): vol.All(vol.Length(1), [STATE_SCHEMA],),
        vol.Required("transitions"): vol.All(
            vol.Length(1), [TRANSITION_SCHEMA],
        ),
    }
)

