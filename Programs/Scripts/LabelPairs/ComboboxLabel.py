import ttkbootstrap as ttk
from ttkwidgets.autocomplete import AutocompleteCombobox


class ComboboxLabel(ttk.Frame):
    def __init__(self, parent, label_text='', combobox_values=(), state='normal', auto=True):

        super().__init__(master=parent)
        self.label = ttk.Label(self, text=label_text)
        self.label.pack(side='left')

        self.var = ttk.StringVar()
        if auto:
            self.combobox = AutocompleteCombobox(self, textvariable=self.var, state=state, validate='key',
                                                 validatecommand=(self.register(self.validate), '%P'))
            self.combobox.configure(postcommand=lambda: self.update_combobox(combobox_values))
        else:
            self.combobox = ttk.Combobox(self, textvariable=self.var, state=state, validate='key',
                                         validatecommand=(self.register(self.validate), '%P'))

        self.combobox['values'] = combobox_values
        self.combobox.pack(side='right')

    def update_combobox(self, new_values):
        self.combobox.configure(completevalues=new_values)

    def validate(self, inp):
        for value in self.combobox['values']:
            if inp in value:
                return True
        return False
