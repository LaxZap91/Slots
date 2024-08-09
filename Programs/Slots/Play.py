from dataclasses import dataclass, field
from .Machine import Machine
from babel.numbers import format_currency 
from typing import Optional
from decimal import Decimal
import datetime
import pathlib
from ttkbootstrap import StringVar

def d(str):
    TWOPLACES = Decimal(10)**-2
    return Decimal(str).quantize(TWOPLACES)

@dataclass
class HandPay():
    pay_amount: Decimal
    tip_amount: Decimal
    image: str = None
    addl_images: list[str] = field(default_factory=list)
    taxable: bool = True

    @property
    def tax(self):
        tax = "0.00"
        if (self.taxable):
            tax = d(d(0.27) * self.pay_amount)
        return tax

@dataclass(repr=False, eq=False, kw_only=True)
class Play:
    machine: Machine
    casino: str = None 
    session_date: datetime = None 
    start_time: datetime = datetime.MINYEAR
    end_time: datetime = datetime.MINYEAR
    _cash_in: list[Decimal] = field(default_factory=list)
    cash_in: Decimal = field(default=Decimal(0.00))
    bet: Decimal = None
    play_type: str = None
    denom: str = None
    state: str = ""
    note: str = None
    start_image: str = None
    addl_images: list[str] = field(default_factory=list)
    end_image: str = None
    cash_out: Decimal = Decimal(0.0)
    hand_pays: list[HandPay] = field(default_factory=list)
    identifier: str = None

    @property
    def identifier(self):
        return f"{self.machine.get_name().replace(' ', '_')}-{self.bet}-{self.start_time.strftime('%Y-%m-%d-%H:%M:%S')}"
    @identifier.setter
    def identifier(self, ident):
        pass

    @property 
    def initial_cash_in(self) -> Decimal:
        return self._cash_in[0]

    @property
    def cash_in(self) -> Decimal:
        return sum(self._cash_in)
    @cash_in.setter
    def cash_in(self, val: Decimal) -> None:
        #JEEP: Why do I need to do this?
        if type(val) == Decimal:
            self._cash_in = [val]
        else:
            self._cash_in = [Decimal(0.00)]

    @property
    def pnl(self) -> Decimal:
        hps = sum(hp.pay_amount for hp in self.hand_pays)
        return self.cash_out + hps - self.cash_in

    def add_cash(self, cash: Decimal) -> None:
        if (len(self._cash_in) == 1 and self._cash_in[0] == Decimal(0)):
            self._cash_in[0] = cash
        else:
            self._cash_in.append(cash)

    def cash_out_str(self):
        rv = ""
        if len(self.hand_pays):
            rv = "="
            hps = "+".join(str(hp.pay_amount) for hp in self.hand_pays)
            rv += hps
            rv += "+"
        rv += str(self.cash_out)
        return rv
    
    def add_image(self, img: pathlib.Path) -> None:
        if img not in self.addl_images:
            self.addl_images.append(img)

    def add_images(self, imgs: list[pathlib.Path]) -> None:
        for img in imgs:
            self.add_image(img)

    def make_hand_pay(self, payment, tip, image = None, addl_images = None):
        if not addl_images:
            addl_images = []
        self.hand_pays.append(HandPay(payment, tip, image, addl_images))

    def add_hand_pay(self, handpay: HandPay):
        self.hand_pays.append(handpay)

    def get_entry_fields(self):
        return None

    def get_state_helper(self):
        return None

    def get_csv_rows(self):
        #JEEP: This doesn't belong in this class
        start_date = self.start_time.strftime(r"%m/%d/%Y")
        images = [str(pathlib.PureWindowsPath(f)) for f in self.addl_images]
        
        rows = [(self.session_date.strftime(r"%m/%d/%Y"), self.casino, self.start_time, self.machine.get_name(), format_currency(self.cash_in, 'USD', locale='en_US'), format_currency(self.bet, 'USD', locale='en_US'), self.play_type, self.denom, self.state, self.cash_out_str(), format_currency(self.pnl, 'USD', locale='en_US'), self.note, self.machine.get_family(), self.start_image, self.end_image, images, self.end_time)]
        for hp in self.hand_pays:
            if hp.tax > 0:
                tax =  format_currency(hp.tax, 'USD', locale='en_US')
                images = hp.addl_images if hp.addl_images else ""
                rows.append((self.session_date.strftime(r"%m/%d/%Y"), self.casino, start_date, self.machine.get_name(), tax,"","Tax Consequence", self.denom, format_currency(hp.pay_amount, 'USD', locale="en_US"),"", -1*tax, tax, self.machine.get_family(), hp.image,"",images,""))
            if hp.tip_amount > 0:
                rows.append((self.session_date.strftime(r"%m/%d/%Y"), self.casino, start_date, self.machine.get_name(), format_currency(hp.tip_amount, 'USD', locale='en_US'),"","Tip","","",format_currency(0.00, 'USD', locale='en_US'), format_currency(-1*hp.tip_amount, 'USD', locale='en_US'),"",self.machine.get_family(),"","","",""))
        return rows

    def __str__(self):
        if self.start_time != datetime.MINYEAR:
            start_date = self.start_time.strftime(r"%m/%d/%Y")
        else:
            start_date = "??"
        images = [str(pathlib.PureWindowsPath(f)) for f in self.addl_images]
        
        outstr = f"{self.identifier},{self.casino},{start_date},{self.machine.get_name()},{format_currency(self.cash_in, 'USD', locale='en_US')},{format_currency(self.bet, 'USD', locale='en_US')},{self.play_type},{self.denom},\"{self.state}\",{self.cash_out_str()},{format_currency(self.pnl, 'USD', locale='en_US')},\"{self.note}\",{self.machine.get_family()},{self.start_image},{self.end_image},{images}"
        for hp in self.hand_pays:
            if hp.tax > 0:
                tax =  format_currency(hp.tax, 'USD', locale='en_US')
                images = hp.addl_images if hp.addl_images else ""
                outstr += f"\n{self.identifier},{self.casino},{start_date},{self.machine.get_name()},{tax},,Tax Consequence,{self.denom},{format_currency(hp.pay_amount, 'USD', locale="en_US")},,-{tax},{tax},{self.machine.get_family()},{hp.image},,{images}"
            if hp.tip_amount > 0:
                outstr += f"\n{self.identifier},{self.casino},{start_date},{self.machine.get_name()},{format_currency(hp.tip_amount, 'USD', locale='en_US')},,Tip,,,{format_currency(0.00, 'USD', locale='en_US')},{format_currency(-1*hp.tip_amount, 'USD', locale='en_US')},,{self.machine.get_family()},,,"
        return outstr
