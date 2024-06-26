import ttkbootstrap as ttk

class LargeEntryLabel(ttk.Frame):
    def __init__(self, parent, label_text='', width=30, height=5):
        
        super().__init__(master=parent)
        self.label = ttk.Label(self, text=label_text)
        self.label.pack(side='left', )
        
        self.text = ttk.Text(self, width=width, height=height)
        self.text.pack(side='right')
    
    def get_text(self):
        return self.text.get('1.0', 'end')

    def clear(self):
        self.text.delete(1.0, ttk.END)