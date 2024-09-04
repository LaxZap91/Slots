import ttkbootstrap as ttk
from ttkbootstrap.widgets import DateEntry

class DateEntryLabel(ttk.Frame):
    def __init__(self, parent, label_text='', entry_var=None, state='normal', callback=None, dateformat=r'%Y-%m-%d'):
        
        super().__init__(master=parent)
        if entry_var is None:
            self.var = ttk.StringVar()
        else:
            self.var = entry_var
        
        self.label = ttk.Label(self, text=label_text)
        self.label.grid(row=0, column=0, sticky='w')
        
        self.date_entry = DateEntry(self, dateformat=dateformat)
        self.date_entry.entry.configure(textvariable=self.var, state=state)
        self.date_entry.grid(row=0, column=1, sticky='e')
        
        self.callback = callback
    
    def execute(self):
        self.callback(self.var.get())