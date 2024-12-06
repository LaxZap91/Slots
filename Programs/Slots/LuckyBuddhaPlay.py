from dataclasses import dataclass, field

from .Machine import Machine
from .StateHelperPlay import StateHelperPlay


@dataclass(repr=False, eq=False)
class LuckyBuddhaPlay(StateHelperPlay):
    machine: Machine = Machine("Lucky Buddha", "Lucky Buddha/Lucky Wealth Cat")
    state_data: dict = field(init=False, default_factory = lambda: {"7xBuddha": None, "6xTurtle": None, "5xCat": None, "3xA": None, "3xK": None, "3xQ": None})
    _state: str = field(init=False)
