import datetime
import pathlib
from decimal import Decimal

import pytest

from Programs.Slots.LuckyWealthCatPlay import LuckyWealthCatPlay
from Programs.tests.test_Play import TestPlay


class TestLuckyWealthCat(TestPlay):
    @pytest.fixture
    def play(self):
        return LuckyWealthCatPlay()

    def test_machine(self, play):
        assert play.machine.get_name() == "Lucky Wealth Cat"
        assert play.machine.get_family() == "Lucky Buddha/Lucky Wealth Cat"

    def test_state_none_not_printed(self, play):
        play.state_data["7xCat"] = 1
        play.state_data["6xFish"] = 2
        play.state_data["5xTree"] = 4
        # play.state_data["3xA"]  left alone
        play.state_data["3xK"] = 1
        play.state_data["3xQ"] = 3

        expected = '{"7xCat": 1, "6xFish": 2, "5xTree": 4, "3xK": 1, "3xQ": 3}'
        assert play.state == expected

    def test_state(self, play):
        play.state_data["7xCat"] = 1
        play.state_data["6xFish"] = 2
        play.state_data["5xTree"] = 4
        play.state_data["3xA"] = 1
        play.state_data["3xK"] = 3
        play.state_data["3xQ"] = 5

        expected = '{"7xCat": 1, "6xFish": 2, "5xTree": 4, "3xA": 1, "3xK": 3, "3xQ": 5}'
        assert play.state == expected

    def test_state_state_plus_details(self, play):
        play.state = "This was a play."
        play.state_data["7xCat"] = 1
        play.state_data["6xFish"] = 2
        play.state_data["5xTree"] = 4
        play.state_data["3xA"] = 1
        play.state_data["3xK"] = 3
        play.state_data["3xQ"] = 5

        expected = 'This was a play.; {"7xCat": 1, "6xFish": 2, "5xTree": 4, "3xA": 1, "3xK": 3, "3xQ": 5}'
        assert play.state == expected

    def test_get_entry_fields(self, play):
        actual = play.get_entry_fields()
        assert len(actual) == 6
        assert actual[0].label == "7xCat"
        actual[0].callback(1)
        assert actual[1].label == "6xFish"
        actual[1].callback(2)
        assert actual[2].label == "5xTree"
        actual[2].callback(4)
        assert actual[3].label == "3xA"
        actual[3].callback(1)
        assert actual[4].label == "3xK"
        actual[4].callback(3)
        assert actual[5].label == "3xQ"
        actual[5].callback(5)

        expected = '{"7xCat": 1, "6xFish": 2, "5xTree": 4, "3xA": 1, "3xK": 3, "3xQ": 5}'
        assert play.state == expected

    def test_play_as_str_no_hp(self, play):
        casino = 'ilani'
        play.casino = casino
        d = datetime.datetime(2024, 1, 2, 3, 4, 5)
        play.start_time = d
        play.add_cash(Decimal(100.0))
        play.add_cash(Decimal(500.0))
        play.bet = Decimal("0.60")
        play.play_type = "AP"
        play.denom = "1cent"
        state = "This; is (a): state"
        play.state = state
        play.cash_out = Decimal("12.34")
        note = "This; is (a): note."
        play.note = note
        simg = r"d:\this\is\a\path\simage.png"
        play.start_image = simg
        eimg = r"d:\this\is\a\path\eimage.png"
        play.end_image = eimg
        img1 = pathlib.Path(r"d:\this\is\a\path\image1.png")
        play.add_image(img1)
        img2 = pathlib.Path(r"d:\this\is\a\path\image2.png")
        img3 = pathlib.Path(r"d:\this\is\a\path\image3.png")
        play.add_images([img2, img3])

        expected = r"""Lucky_Wealth_Cat-0.60-2024-01-02-03:04:05,ilani,01/02/2024,Lucky Wealth Cat,$600.00,$0.60,AP,1cent,"This; is (a): state",12.34,-$587.66,"This; is (a): note.",Lucky Buddha/Lucky Wealth Cat,d:\this\is\a\path\simage.png,d:\this\is\a\path\eimage.png,['d:\\this\\is\\a\\path\\image1.png', 'd:\\this\\is\\a\\path\\image2.png', 'd:\\this\\is\\a\\path\\image3.png']"""

        assert str(play) == expected

    def test_play_as_str_with_hp(self, play):
        pass
