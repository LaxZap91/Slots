from dataclasses import dataclass, field

from .Machine import Machine
from .StateHelperPlay import StateHelperPlay


@dataclass(repr=False, eq=False)
class UltraRushGoldPlay(StateHelperPlay):
    machine: Machine = Machine("Ultra Rush Gold", "Ultra Rush Gold")
    state_data: dict = field(init=False,
                             default_factory=lambda: {"Spins": None, "Number of Gold": None, "Ball 1 Val": None,
                                                      "Ball 2 Val": None, "Ball 3 Val": None, "Ball 4 Val": None,
                                                      "Ball 5 Val": None})

    @property
    def state(self) -> str:
        rv = {k: v for k, v in self.state_data.items() if v and v != ""}
        if not len(rv):
            return self._state

        spins = self.state_data['Spins']
        if not spins:
            spins = "?"

        golds = []
        for k in ["Ball 1 Val", "Ball 2 Val", "Ball 3 Val", "Ball 4 Val", "Ball 5 Val"]:
            if k in self.state_data and self.state_data[k]:
                golds.append(self.state_data[k])

        if "Number of Gold" in self.state_data:
            ngolds = self.state_data['Number of Gold']
        else:
            ngolds = len(golds)

        helper_str = f"{spins} spins; {ngolds} gold ({golds})"
        if self._state.strip() != "":
            return "; ".join([self._state.strip(), helper_str])
        return helper_str

    @state.setter
    def state(self, state):
        self._state = state.strip()
