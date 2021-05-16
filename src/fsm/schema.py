import voluptuous as vol

CB_SCHEMA = vol.Schema(vol.Any(str, [str]))

# validation schema for State object initialization data
STATE_SCHEMA = vol.Schema(
    vol.Any(
        str,
        {
            "name": str,
            vol.Optional("on_enter"): CB_SCHEMA,
            vol.Optional("on_exit"): CB_SCHEMA,
        },
    )
)

# validation schema for Transition object initialization data
TRANSITION_SCHEMA = vol.Schema(
    {
        vol.Required("action"): str,
        vol.Required("from_state"): str,
        vol.Required("to_state"): str,
        vol.Optional("on_before"): CB_SCHEMA,
        vol.Optional("on_after"): CB_SCHEMA,
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

