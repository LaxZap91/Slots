from dataclasses import dataclass, field

from .Machine import Machine
from .StateHelperPlay import StateHelperPlay


@dataclass(repr=False, eq=False)
class PinwheelPrizesPlay(StateHelperPlay):
    machine: Machine = Machine("Pinwheel Prizes", "Pinwheel Prizes")
    state_data: dict = field(init=False, default_factory=lambda: {"Golds": None, "10:1s": None})

    @property
    def state(self) -> str:
        rv = ""
        if self._state.strip() != "":
            rv = f"{self._state.strip()}; "
        if self.state_data["Golds"]:
            individual = [int(i) for i in list(self.state_data["Golds"])]
            tot = sum(individual)
            rv = f'{rv}{tot} {self.state_data["Golds"]}'
        if self.state_data["10:1s"]:
            rv = f'{rv}/{self.state_data["10:1s"]}'
        return rv

    @state.setter
    def state(self, state):
        self._state = state
