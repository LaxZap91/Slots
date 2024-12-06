import ttkbootstrap as ttk


class LabelLabel(ttk.Frame):
    def __init__(self, parent, label_text='', label_text_var='', label_var=None):
        if label_var is None:
            self.var = ttk.StringVar(value=label_text_var)
        else:
            self.var = label_var

        super().__init__(master=parent)
        self.label = ttk.Label(self, text=label_text)
        self.label.grid(row=0, column=0, padx=5, pady=5)
        # self.label.pack(side='left', )

        self.entry = ttk.Label(self, textvariable=self.var)
        # self.entry.pack(side='right')
        self.entry.grid(row=0, column=1, padx=5, pady=5)
