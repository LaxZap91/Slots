import ttkbootstrap as ttk

import tkinter as tk
from Slots.Play import HandPay

from Scripts.LabelPairs.MoneyEntryLabel import MoneyEntryLabel
from decimal import Decimal


class HandPayWindow(tk.Toplevel):
    def __init__(self, *args, callback=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback
        self.handpay = None
        self.title('Handpay/Ticket Out')
        self.minsize(300, 300)
        self.iconphoto(False, ttk.PhotoImage(file=r'Programs\Icon\slot_machine_icon.png'))
        self.handpay = MoneyEntryLabel(self, 'Money Received')
        self.handpay.pack()
        self.tip = MoneyEntryLabel(self, 'Tip amount')
        self.tip.pack()

        self.taxable = tk.BooleanVar(value=True)
        self.taxable_btn = ttk.Checkbutton(self, text="Taxable", onvalue=True, offvalue=False, variable=self.taxable)
        self.taxable_btn.pack()

        self.okay_button = ttk.Button(
            self,
            text="Okay",
            command=self.button_okay_pressed
        )
        self.okay_button.pack()
        self.cancel_button = ttk.Button(
            self,
            text="Cancel",
            command=self.button_cancel_pressed
        )
        self.cancel_button.pack()
        self.focus()

    def button_okay_pressed(self):
        hp = HandPay(Decimal(self.handpay.var.get()), Decimal(self.tip.var.get()), taxable=self.taxable.get())
        self.callback(hp)
        self.destroy()

    def button_cancel_pressed(self):
        self.destroy()
