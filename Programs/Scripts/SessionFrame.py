import ttkbootstrap as ttk

from Scripts.LabelPairs.ComboboxLabel import ComboboxLabel


def _no_tab(_, parent):
    # focuses on the next wigit
    parent.focus_get().tk_focusNext().focus()
    return 'break'


def _no_shift_tab(_, parent):
    # focuses on the previous wigit
    parent.focus_get().tk_focusPrev().focus()
    return 'break'


class SessionFrame(ttk.Frame):
    def __init__(self, parent, window):
        super().__init__(master=parent)
        self._window = window

        self._create_header()
        self._create_entries()
        self._place_entries()

    def _create_header(self):
        self._header = ttk.Label(self, text="Session Information", anchor='center')

    def _create_entries(self):
        self._create_session_date()
        self._create_casino()

    def _create_session_date(self):
        self.session_date = ttk.Label(self, textvariable=self._window.session_date)

    def _create_casino(self):
        self.casino = ComboboxLabel(self, '', self._window.casino_values, state='readonly')

    def _place_entries(self):
        self._header.grid(row=0, columnspan=2, pady=5)
        self.casino.grid(row=1, column=0, padx=5, pady=5)
        self.session_date.grid(row=1, column=1, padx=5, pady=5)
