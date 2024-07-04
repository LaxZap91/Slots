import pytest
import datetime
import pathlib
from decimal import Decimal

from Programs.Slots.Machine import Machine
from Programs.Slots.Play import Play
from Programs.Slots.LuckyWealthCatPlay import LuckyWealthCatPlay


machine_for_test = Machine("Test Machine")
class TestPlay():
    @pytest.fixture
    def play(self):
        return Play(machine_for_test)

    def test_casino(self, play):
        assert play.casino is None 
        casino = 'ilani'
        play.casino = casino
        assert play.casino == casino
    
    def test_start_time(self, play):
        assert play.start_time == datetime.MINYEAR
        d = datetime.datetime(2024, 1,2,3,4,5)
        play.start_time = d
        assert play.start_time == d

    def test_machine(self, play):
        m = Machine("non-existant", "non-existant")
        assert play.machine != m
        assert play.machine == machine_for_test
        
    def test_add_cash(self, play):
        assert play.cash_in == 0
        play.add_cash(100)
        assert play.cash_in == Decimal(100)
        play.add_cash(500)
        assert play.cash_in == Decimal(600)
        #assert play.initial_cash_in == Decimal("12.34")

    def test_initial_cash_in(self, play):
        assert play.cash_in == 0
        play.add_cash(Decimal("12.34"))
        assert play.cash_in == Decimal("12.34")
    
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
        assert play.note == None
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
        assert play.start_image == None
        img = "d:\\this\\is\\a\\path\\image.png"
        play.start_image = img
        assert play.start_image == img
    
    def test_end_image(self, play):
        assert play.end_image == None
        img = "d:\\this\\is\\a\\path\\image.png"
        play.end_image = img
        assert play.end_image == img
    
    def test_add_image(self, play):
        assert play.addl_images == []
        img1 = "d:\\this\\is\\a\\path\\image.png"
        img2 = "d:\\this\\is\\a\\path\\image2.png"
        img3 = "d:\\this\\is\\a\\path\\image3.png"
        play.add_image(img1)
        assert play._addl_images == [img1]
        play.add_image(img2)
        assert play._addl_images == [img1, img2]
        play.add_image(img3)
        assert play.addl_images == [img1, img2, img3]
    
    def test_add_image(self, play):
        assert play.addl_images == []
        img1 = "d:\\this\\is\\a\\path\\image.png"
        img2 = "d:\\this\\is\\a\\path\\image2.png"
        img3 = "d:\\this\\is\\a\\path\\image3.png"
        play.add_images([img1, img2, img3])
        assert play.addl_images == [img1, img2, img3]
    
    def test_play_as_str(self, play):
        casino = 'ilani'
        play.casino = casino
        d = datetime.datetime(2024, 1,2,3,4,5)
        play.start_time = d
        play.add_cash(100)
        play.add_cash(500)
        play.bet = Decimal("0.60")
        play.play_type = "AP"
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

        expected = r"""ilani,01/02/2024,Test Machine,$600.00,$0.60,AP,"This; is (a): state",$12.34,-$587.66,"This; is (a): note.",Test Machine,d:\this\is\a\path\simage.png,d:\this\is\a\path\eimage.png,['d:\\this\\is\\a\\path\\image1.png', 'd:\\this\\is\\a\\path\\image2.png', 'd:\\this\\is\\a\\path\\image3.png']"""

        assert str(play) == expected