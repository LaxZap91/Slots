from .LuckyWealthCatPlay import LuckyWealthCatPlay
from .LuckyBuddhaPlay import LuckyBuddhaPlay
from .PowerPushPlay import PowerPushPlay
from .PinwheelPrizesPlay import PinwheelPrizesPlay
from .FrankensteinPlay import FrankensteinPlay
from .UltraRushGoldPlay import UltraRushGoldPlay
from .RichLittlePiggiesPlay import RichLittlePiggiesPlay, RichLittlePiggiesHogWildPlay, RichLittlePiggiesMealTicketPlay
from .Machine import Machine
from .Play import Play


class PlayFactory:
    play_for_machine = {
        "Frankenstein": FrankensteinPlay,
        "Frankenstein (Bingo)": FrankensteinPlay,
        "Lucky Wealth Cat": LuckyWealthCatPlay,
        "Lucky Wealth Cat (Bingo)": LuckyWealthCatPlay,
        "Lucky Buddha": LuckyBuddhaPlay,
        "Lucky Buddha (Bingo)": LuckyBuddhaPlay,
        "Pinwheel Prizes": PinwheelPrizesPlay,
        "Pinwheel Prizes (Bingo)": PinwheelPrizesPlay,
        "Power Push": PowerPushPlay,
        "Power Push (Bingo)": PowerPushPlay,
        "Rich Little Piggies": RichLittlePiggiesPlay,
        "Rich Little Piggies (Bingo)": RichLittlePiggiesPlay,
        "Rich Little Piggies Hog Wild": RichLittlePiggiesHogWildPlay,
        "Rich Little Piggies Hog Wild (Bingo)": RichLittlePiggiesHogWildPlay,
        "Rich Little Piggies Meal Ticket": RichLittlePiggiesMealTicketPlay,
        "Rich Little Piggies Meal Ticket (Bingo)": RichLittlePiggiesMealTicketPlay,
        "Ultra Rush Gold": UltraRushGoldPlay,
        "Ultra Rush Gold (Bingo)": UltraRushGoldPlay}

    @staticmethod
    def get_play(machine_name: str) -> Play:
        if machine_name in PlayFactory.play_for_machine:
            return PlayFactory.play_for_machine[machine_name]()
        return Play(machine=Machine(machine_name))
