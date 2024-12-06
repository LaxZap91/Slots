import ttkbootstrap as ttk


class EntryLabel(ttk.Frame):
    def __init__(self, parent, label_text='', entry_var=None, state='normal', callback=None):
        super().__init__(master=parent)
        if entry_var is None:
            self.var = ttk.StringVar()
        else:
            self.var = entry_var

        self.label = ttk.Label(self, text=label_text)
        self.label.grid(row=0, column=0, sticky='w')
        # self.label.pack(side='left')

        self.entry = ttk.Entry(self, textvariable=self.var, state=state)
        self.entry.grid(row=0, column=1, sticky='e')
        # self.entry.pack(side='right')

        self.callback = callback

    def execute(self):
        self.callback(self.var.get())
