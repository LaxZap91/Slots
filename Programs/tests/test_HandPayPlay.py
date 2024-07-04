import pytest
import datetime
import pathlib
from decimal import Decimal

from Programs.Slots.Machine import Machine
from Programs.Slots.TipPlay import TipPlay


machine_for_test = Machine("Test Machine")
class TestTipPlay():
    @pytest.fixture
    def play(self):
        return TipPlay()

#    def test_add_cash(self, play):
#        pass

#    def test_initial_cash_in(self, play):
#        pass
    
    def test_play_type(self, play):
        assert play.play_type == "Tip"
    
#    def test_cash_out(self, play):
#        assert play.cash_out == Decimal(0.0)
    
#    def test_note(self, play):
#        assert play.note == None
#        note = "This; is (a): note."
#        play.note = note
#        assert play.note == note
    
#    def test_play_as_str(self, play):
#        casino = 'ilani'
#        play.casino = casino
#        d = datetime.datetime(2024, 1,2,3,4,5)
#        play.start_time = d
#        play.add_cash(100)
#        play.add_cash(500)
#        play.bet = Decimal("0.60")
#        play.play_type = "AP"
#        state = "This; is (a): state"
#        play.state = state
#        play.cash_out = Decimal("12.34")
#        note = "This; is (a): note."
#        play.note = note
#        simg = r"d:\this\is\a\path\simage.png"
#        play.start_image = simg
#        eimg = r"d:\this\is\a\path\eimage.png"
#        play.end_image = eimg
#        img1 = pathlib.Path(r"d:\this\is\a\path\image1.png")
#        play.add_image(img1)
#        img2 = r"d:\this\is\a\path\image2.png"
#        img3 = r"d:\this\is\a\path\image3.png"
#        play.add_images([img2, img3])
#
#        expected = r"""ilani,01/02/2024,Test Machine,$600.00,$0.60,AP,"This; is (a): state",$12.34,-$587.66,"This; is (a): note.",Test Machine,d:\this\is\a\path\simage.png,d:\this\is\a\path\eimage.png,['d:\\this\\is\\a\\path\\image1.png', 'd:\\this\\is\\a\\path\\image2.png', 'd:\\this\\is\\a\\path\\image3.png']"""
#
#        assert str(play) == expected