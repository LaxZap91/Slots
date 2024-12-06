import ttkbootstrap as ttk


class SessionTable(ttk.Treeview):
    def __init__(self, parent):
        super().__init__(master=parent, columns=('id', 'key'), show='headings')
        self._parent = parent
        self.heading('id', text="idx")
        self.column('id', minwidth=0, width=50, stretch=False)
        self.heading('key', text="Play ID")
        self.column('key', minwidth=0, width=300, stretch=False)
        self.bind('<Delete>', self.delete_play)
        self.bind('<Double-Button-1>', self.load_play)

    def update_table(self):
        self.delete(*self.get_children())
        keys = list(self._parent.plays.keys())
        for index, play_id in enumerate(keys):
            self.insert(parent='', index=ttk.END, values=(index, play_id))

    def delete_play(self, _):
        for item in self.selection():
            value = self.item(item)['values'][1]
            self._parent.remove_play(value)
        self.update_table()

    def load_play(self, _):
        self._parent.load_play(self.item(self.selection(), 'values')[1])

    def clear_selection(self):
        for item in self.selection():
            self.selection_remove(item)
