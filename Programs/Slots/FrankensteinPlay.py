import json
from dataclasses import dataclass, field
from decimal import Decimal

from ttkbootstrap.dialogs import Messagebox

from .Machine import Machine
from .StateHelperPlay import StateHelperPlay


@dataclass(repr=False, eq=False)
class FrankensteinPlay(StateHelperPlay):
    machine: Machine = Machine("Frankenstein", "Frankenstein")
    state_data: dict = field(init=False,
                             default_factory=lambda: {"tl": None, "tm": None, "tr": None, "ml": None, "mm": None,
                                                      "mr": None, "bl": None, "bm": None, "br": None})

    @staticmethod
    def d(in_str):
        TWOPLACES = Decimal(10) ** -2
        return Decimal(in_str).quantize(TWOPLACES)

    states = {
        (d("0.6"), "1cent"): {1000: None, 500: None, 300: None, 200: None, 150: None, 125: None, 100: None, 75: None,
                              60: None},
        (d("1.2"), "1cent"): {2000: None, 1000: None, 600: None, 400: None, 300: None, 250: None, 200: None, 150: None,
                              120: None},
        (d("1.8"), "1cent"): {3000: None, 1500: None, 900: None, 600: None, 450: None, 375: None, 300: None, 225: None,
                              180: None},
        (d("3"), "1cent"): {5000: None, 2500: None, 1500: None, 1000: None, 750: None, 625: None, 500: None, 375: None,
                            300: None},
        (d("6"), "1cent"): {10000: None, 5000: None, 3000: None, 2000: None, 1500: None, 1250: None, 1000: None,
                            750: None, 600: None},
        (d("1.2"), "2cent"): {1000: None, 500: None, 300: None, 200: None, 150: None, 125: None, 100: None, 75: None,
                              60: None},
        (d("2.4"), "2cent"): {2000: None, 1000: None, 600: None, 400: None, 300: None, 250: None, 200: None, 150: None,
                              120: None},
        (d("3.6"), "2cent"): {3000: None, 1500: None, 900: None, 600: None, 450: None, 375: None, 300: None, 225: None,
                              180: None},
        (d("6"), "2cent"): {5000: None, 2500: None, 1500: None, 1000: None, 750: None, 625: None, 500: None, 375: None,
                            300: None},
        (d("12"), "2cent"): {10000: None, 5000: None, 3000: None, 2000: None, 1500: None, 1250: None, 1000: None,
                             750: None, 500: None},
        (d("1.5"), "5cent"): {500: None, 250: None, 150: None, 100: None, 75: None, 60: None, 50: None, 40: None,
                              30: None},
        (d("3"), "5cent"): {1000: None, 500: None, 300: None, 200: None, 150: None, 120: None, 80: None, 60: None,
                            90: None},
        (d("4.5"), "5cent"): {1500: None, 750: None, 450: None, 300: None, 225: None, 180: None, 150: None, 120: None,
                              90: None},
        (d("7.5"), "5cent"): {2500: None, 1250: None, 750: None, 500: None, 375: None, 300: None, 250: None, 200: None,
                              150: None},
        # (d("max"), "5cent"): {},
        (d("3"), "10cent"): {500: None, 250: None, 150: None, 100: None, 75: None, 60: None, 50: None, 40: None,
                             30: None},
        (d("6"), "10cent"): {1000: None, 500: None, 300: None, 200: None, 150: None, 120: None, 100: None, 80: None,
                             60: None},
        (d("9"), "10cent"): {1500: None, 750: None, 450: None, 300: None, 225: None, 180: None, 150: None, 120: None,
                             90: None},
        (d("15"), "10cent"): {2500: None, 1250: None, 750: None, 500: None, 375: None, 300: None, 250: None, 200: None,
                              150: None},
        # (d("max"), "10cent"): {},
        (d("5"), "$1"): {75: None, 40: None, 25: None, 20: None, 15: None, 10: None, 8: None, 6: None, 5: None},
        (d("10"), "$1"): {150: None, 80: None, 50: None, 40: None, 30: None, 20: None, 16: None, 12: None, 10: None},
        (d("15"), "$1"): {225: None, 120: None, 75: None, 60: None, 45: None, 30: None, 24: None, 18: None, 15: None},
        (d("20"), "$1"): {300: None, 160: None, 100: None, 80: None, 60: None, 40: None, 32: None, 24: None, 20: None},
        (d("25"), "$1"): {375: None, 200: None, 125: None, 100: None, 75: None, 50: None, 40: None, 30: None, 25: None},
        # (d("min"), "$2"): {},
        # (d("min2"), "$2"): {},
        (d("10"), "$2"): {150: None, 80: None, 50: None, 40: None, 30: None, 20: None, 16: None, 12: None, 10: None},
        (d("20"), "$2"): {300: None, 160: None, 100: None, 80: None, 60: None, 40: None, 32: None, 24: None, 20: None},
        (d("50"), "$2"): {750: None, 400: None, 250: None, 200: None, 150: None, 100: None, 80: None, 60: None,
                          50: None},
    }

    def get_state_data(self):
        if not self.denom or not self.bet:
            Messagebox.show_error("You must set both the denom and bet first")
            return False
        if (FrankensteinPlay.d(self.bet), self.denom) not in self.states:
            Messagebox.show_error(f"This combination of {self.bet} bet and {self.denom} denom is not known")
            return False
        self.state_data = self.states[(FrankensteinPlay.d(self.bet), self.denom)]
        return True

    def get_entry_fields(self) -> list:
        if self.get_state_data():
            return super().get_entry_fields()
        return []

    @property
    def state(self) -> str:
        rv = {k: int(v) for k, v in self.state_data.items() if v and v != ""}
        if not len(rv):
            return self._state

        john = sum(rv.values())
        dave = sum(rv.values()) + (9 - len(rv.keys()))

        if self._state.strip() != "":
            return "; ".join([self._state.strip(), json.dumps(rv), f" [j:{john}; d:{dave}]"])
        return "; ".join([json.dumps(rv), f" [j:{john}; d:{dave}]"])

    @state.setter
    def state(self, state):
        self._state = state.strip()
