from dataclasses import dataclass, field

from .LuckyBuddhaPlay import LuckyBuddhaPlay
from .Machine import Machine


@dataclass(repr=False, eq=False)
class LuckyWealthCatPlay(LuckyBuddhaPlay):
    machine: Machine = Machine("Lucky Wealth Cat", "Lucky Buddha/Lucky Wealth Cat")
    state_data: dict = field(init=False,
                             default_factory=lambda: {"7xCat": None, "6xFish": None, "5xTree": None, "3xA": None,
                                                      "3xK": None, "3xQ": None})
