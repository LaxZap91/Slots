import tkinter as tk

import ttkbootstrap as ttk

from Scripts.LabelPairs.EntryLabel import EntryLabel
from Slots.Play import Play


class StateEntryHelperWindow(tk.Toplevel):
    def __init__(self, *args, play: Play, **kwargs):
        self.fields = play.get_entry_fields()
        if self.fields is None:
            return

        super().__init__(*args, **kwargs)
        self.title('State Entry')
        self.minsize(300, 300)
        self.iconphoto(False, ttk.PhotoImage(file=r'Programs\Icon\slot_machine_icon.png'))

        self.entries = []
        for f in self.fields:
            lbl = EntryLabel(self, f.label, callback=f.callback)
            self.entries.append(lbl)
            lbl.pack()

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
        for e in self.entries:
            e.execute()
        self.destroy()

    def button_cancel_pressed(self):
        self.destroy()
