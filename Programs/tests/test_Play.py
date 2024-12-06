import datetime
import pathlib
from decimal import Decimal

import pytest

from Programs.Slots.Machine import Machine
from Programs.Slots.Play import Play, HandPay

machine_for_test = Machine("Test Machine")


class TestPlay:
    @pytest.fixture
    def play(self):
        return Play(machine=machine_for_test)

    def test_casino(self, play):
        assert play.casino is None
        casino = 'ilani'
        play.casino = casino
        assert play.casino == casino

    def test_start_time(self, play):
        assert play.start_time == datetime.MINYEAR
        d = datetime.datetime(2024, 1, 2, 3, 4, 5)
        play.start_time = d
        assert play.start_time == d

    def test_machine(self, play):
        m = Machine("non-existant", "non-existant")
        assert play.machine != m
        assert play.machine == machine_for_test

    def test_add_cash(self, play):
        assert play.initial_cash_in == Decimal(0.00)
        play.add_cash(Decimal(100.00))
        assert play.cash_in == Decimal(100)
        play.add_cash(Decimal(500.00))
        assert play.cash_in == Decimal(600)
        # assert play.initial_cash_in == Decimal("12.34")

    def test_initial_cash_in(self, play):
        assert play.initial_cash_in == Decimal(0.00)
        play.add_cash(Decimal("12.34"))
        assert play.initial_cash_in == Decimal("12.34")

    def test_initial_cash_in_defaults_0(self, play):
        assert play.cash_in == Decimal(0.00)
        assert play.initial_cash_in == Decimal("0.00")

    def test_bet(self, play):
        assert play.bet is None
        play.bet = Decimal("0.60")
        assert play.bet == Decimal("0.60")

    def test_play_type(self, play):
        assert play.play_type is None
        play.play_type = "AP"
        assert play.play_type == "AP"

    def test_state(self, play):
        assert play.state == ""
        state = "This; is (a): state"
        play.state = state
        assert play.state == state

    def test_cash_out(self, play):
        assert play.cash_out == Decimal(0.0)
        play.cash_out = Decimal("12.34")
        assert play.cash_out == Decimal("12.34")

    def test_note(self, play):
        assert play.note is None
        note = "This; is (a): note."
        play.note = note
        assert play.note == note

    pnl_testdata = [
        (100, 112, 12.00),
        (100, 0, -100),
        (500, 400, -100),
        (500, Decimal("399.99"), Decimal("-100.01"))
    ]

    @pytest.mark.parametrize("cash_in, cash_out, expected", pnl_testdata)
    def test_pnl(self, play, cash_in, cash_out, expected):
        assert play.pnl == 0.0
        play.add_cash(cash_in)
        play.cash_out = cash_out
        assert play.pnl == expected

    def test_start_image(self, play):
        assert play.start_image is None
        img = "d:\\this\\is\\a\\path\\image.png"
        play.start_image = img
        assert play.start_image == img

    def test_end_image(self, play):
        assert play.end_image is None
        img = "d:\\this\\is\\a\\path\\image.png"
        play.end_image = img
        assert play.end_image == img

    def test_add_image(self, play):
        assert play.addl_images == []
        img1 = "d:\\this\\is\\a\\path\\image.png"
        img2 = "d:\\this\\is\\a\\path\\image2.png"
        img3 = "d:\\this\\is\\a\\path\\image3.png"
        play.add_image(img1)
        assert play.addl_images == [img1]
        play.add_image(img2)
        assert play.addl_images == [img1, img2]
        play.add_image(img3)
        assert play.addl_images == [img1, img2, img3]

    def test_add_image2(self, play):
        assert play.addl_images == []
        img1 = "d:\\this\\is\\a\\path\\image.png"
        img2 = "d:\\this\\is\\a\\path\\image2.png"
        img3 = "d:\\this\\is\\a\\path\\image3.png"
        play.add_images([img1, img2, img3])
        assert play.addl_images == [img1, img2, img3]

    def test_play_as_str_no_hp(self, play):
        casino = 'ilani'
        play.casino = casino
        d = datetime.datetime(2024, 1, 2, 3, 4, 5)
        play.start_time = d
        play.add_cash(100)
        play.add_cash(500)
        play.bet = Decimal("0.60")
        play.play_type = "AP"
        play.denom = "$1"
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
        img2 = r"d:\this\is\a\path\image2.png"
        img3 = r"d:\this\is\a\path\image3.png"
        play.add_images([img2, img3])

        expected = r"""Test_Machine-0.60-2024-01-02-03:04:05,ilani,01/02/2024,Test Machine,$600.00,$0.60,AP,$1,"This; is (a): state",12.34,-$587.66,"This; is (a): note.",Test Machine,d:\this\is\a\path\simage.png,d:\this\is\a\path\eimage.png,['d:\\this\\is\\a\\path\\image1.png', 'd:\\this\\is\\a\\path\\image2.png', 'd:\\this\\is\\a\\path\\image3.png']"""

        assert str(play) == expected

    def test_play_as_str_with_hp(self, play):
        play.casino = 'ilani'
        play.start_time = datetime.datetime(2024, 1, 2, 3, 4, 5)
        play.add_cash(100)
        play.bet = Decimal("10.60")
        play.play_type = "AP"
        play.denom = "1cent"
        play.state = "This; is (a): state"
        play.cash_out = Decimal("1234.56")
        play.note = "This; is (a): note."
        play.start_image = r"d:\this\is\a\path\simage.png"
        play.end_image = r"d:\this\is\a\path\eimage.png"
        play.add_image(pathlib.Path(r"d:\this\is\a\path\image1.png"))
        img2 = r"d:\this\is\a\path\image2.png"
        img3 = r"d:\this\is\a\path\image3.png"
        play.add_images([img2, img3])

        img4 = r"d:\this\is\a\path\image4.png"
        img5 = r"d:\this\is\a\path\image5.png"
        play.make_hand_pay(Decimal(1201.00), Decimal(20.00), img4)
        hp = HandPay(Decimal(2000.00), Decimal(40.00), img4, [img5])
        play.add_hand_pay(hp)

        expected = r"""Test_Machine-10.60-2024-01-02-03:04:05,ilani,01/02/2024,Test Machine,$100.00,$10.60,AP,1cent,"This; is (a): state",=1201+2000+1234.56,$4,335.56,"This; is (a): note.",Test Machine,d:\this\is\a\path\simage.png,d:\this\is\a\path\eimage.png,['d:\\this\\is\\a\\path\\image1.png', 'd:\\this\\is\\a\\path\\image2.png', 'd:\\this\\is\\a\\path\\image3.png']
Test_Machine-10.60-2024-01-02-03:04:05,ilani,01/02/2024,Test Machine,$324.27,,Tax Consequence,1cent,$1,201.00,,-$324.27,$324.27,Test Machine,d:\this\is\a\path\image4.png,,
Test_Machine-10.60-2024-01-02-03:04:05,ilani,01/02/2024,Test Machine,$20.00,,Tip,,,$0.00,-$20.00,,Test Machine,,,
Test_Machine-10.60-2024-01-02-03:04:05,ilani,01/02/2024,Test Machine,$540.00,,Tax Consequence,1cent,$2,000.00,,-$540.00,$540.00,Test Machine,d:\this\is\a\path\image4.png,,['d:\\this\\is\\a\\path\\image5.png']
Test_Machine-10.60-2024-01-02-03:04:05,ilani,01/02/2024,Test Machine,$40.00,,Tip,,,$0.00,-$40.00,,Test Machine,,,"""

        assert str(play) == expected
