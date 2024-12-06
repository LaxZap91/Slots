from dataclasses import dataclass, field

from babel.numbers import format_currency

from Programs.Slots.Machine import Machine
from Programs.Slots.Play import Play


@dataclass(repr=False, eq=False)
class TipPlay(Play):
    machine: Machine = field(default=Machine('Tip', 'Non-AP'), init=False)
    play_type: str = field(default='Tip', init=False)
    _start_image: str = field(default=None, init=False)
    _addl_images: list[str] = field(default=None, init=False)
    _end_image: str = field(default=None, init=False)

    def __str__(self):
        start_date = self.start_time.strftime(r"%m/%d/%Y")
        note = f'"{self.note}"' if self.note else ""
        return f"{self.casino},{start_date},{self.machine.get_name()},{format_currency(self.cash_in, 'USD', locale='en_US')},,{self.play_type},,{format_currency(self.cash_out, 'USD', locale='en_US')},{format_currency(self.pnl, 'USD', locale='en_US')},{note},{self.machine.get_family()},,,"
