from dataclasses import dataclass, field

from .Machine import Machine
from .StateHelperPlay import StateHelperPlay


@dataclass(repr=False, eq=False)
class PowerPushPlay(StateHelperPlay):
    machine: Machine = Machine("Power Push", "Power Push")
    state_data: dict = field(init=False,
                             default_factory=lambda: {"Stacks": None, "Diamonds": None, "Gems": None, "Royals": None,
                                                      "Majors": None, "Minors": None, "Free Spins": None, "Minis": None,
                                                      "Balls": None, "Pearls": None, "+2 Pushes": None})
