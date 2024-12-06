import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame


class ImageDisplay(ScrolledFrame):
    def __init__(self, parent):
        # initializes the frame
        super().__init__(master=parent, autohide=True, height=1000, width=1000)
        # creates the canvas
        self.canvas = ttk.Canvas(master=self, width=1500, height=1500)
        # places the canvas
        self.canvas.pack(fill='both')
