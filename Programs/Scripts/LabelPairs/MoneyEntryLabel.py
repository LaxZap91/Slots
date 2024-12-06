import ttkbootstrap as ttk


def period(_, parent):
    if parent.entry.get() == '':
        parent.entry.insert(ttk.INSERT, '0.')
        return 'break'
    else:
        return


class MoneyEntryLabel(ttk.Frame):
    def __init__(self, parent, label_text=''):

        super().__init__(master=parent)
        self.label = ttk.Label(self, text=label_text)
        self.label.pack(side='left')

        self.var = ttk.StringVar(value="0")
        self.entry = ttk.Entry(self, textvariable=self.var, validate='key',
                               validatecommand=(self.register(self.validate), '%P'), width=10)
        self.entry.pack(side='right')

        self.entry.bind('.', lambda _: period(_, self))

    def validate(self, inp):
        try:
            if str(inp) == '':
                return True

            float(inp)
            split_inp = inp.split('.')

            if len(split_inp) > 2:
                return False
            if len(split_inp) == 2 and len(split_inp[1]) > 2:
                return False
        except Exception:
            return False
        return True

    def get_var(self):
        try:
            val = self.var.get()
        except Exception:
            val = 0
        return val
