import datetime

from babel.numbers import format_currency

from Programs.Slots.Play import Play

casinos = ['ilani', 'Spirit Mountain']

field_types = ['str', 'float', 'int']


class Session:
    def __init__(self):
        self.start = None
        self.plays = [Play]

    def set_start(self, start_time: datetime):
        self.start = start_time

    def get_pnl(self) -> float:
        return sum([p.pnl for p in self.plays])

    def add_play(self, play, check_consistency=True) -> tuple[int, str]:
        warning = ""
        if (len(self.plays) > 0 and format_currency(self.plays[-1].cash_out_str(), "USD", locale='en_US') !=
                format_currency(play.get_initial_cash_in(), "USD", locale='en_US')):
            warning = "This play starts with a different amount than the previous play\n"

        if check_consistency and warning != "":
            return -1, warning

        self.plays.append(play)
        return 0, warning
