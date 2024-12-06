from dataclasses import dataclass, field

from .Machine import Machine
from .StateHelperPlay import StateHelperPlay


@dataclass(repr=False, eq=False)
class RichLittlePiggiesPlay(StateHelperPlay):
    machine: Machine = Machine("Rich Little Piggies Hog Wild", "Rich Little Piggies")
    state_data: dict = field(init=False, default_factory=lambda: {"Blue": None, "Red": None})
    _state: str = field(init=False)

    def get_red_str(self):
        if self.state_data["Red"]:
            return f"; Red: {self.state_data['Red']}"
        return ""

    @property
    def state(self) -> str:
        rv = {k: v for k, v in self.state_data.items() if v and v != ""}
        if not len(rv):
            return self._state

        blues = "?"
        if rv["Blue"]:
            blues = rv["Blue"]
        state_str = f"{blues} blue"

        reds = self.get_red_str()
        state_str += reds

        if self._state.strip() != "":
            return "; ".join([self._state.strip(), state_str])
        return state_str

    @state.setter
    def state(self, state):
        self._state = state.strip()


@dataclass(repr=False, eq=False)
class RichLittlePiggiesHogWildPlay(RichLittlePiggiesPlay):
    machine: Machine = Machine("Rich Little Piggies Hog Wild", "Rich Little Piggies")
    state_data: dict = field(init=False, default_factory=lambda: {"Blue": None, "Red(#wilds)": None})
    _state: str = field(init=False)

    def get_red_str(self):
        if self.state_data["Red(#wilds)"]:
            return f"; {self.state_data['Red(#wilds)']} wilds"
        return ""


@dataclass(repr=False, eq=False)
class RichLittlePiggiesMealTicketPlay(RichLittlePiggiesPlay):
    machine: Machine = Machine("Rich Little Piggies Meal Ticket", "Rich Little Piggies")
    state_data: dict = field(init=False, default_factory=lambda: {"Blue": None, "X'd Red(TJQKAB)": None})
    _state: str = field(init=False)

    def get_red_str(self):
        red_key = "X'd Red(TJQKAB)"
        if self.state_data[red_key]:
            return f"; {self.state_data[red_key]}"
        return ""
