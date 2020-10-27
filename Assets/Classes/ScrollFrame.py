from tkinter import Canvas
from tkinter import ttk


# scrollFrame Class extends ttk.LabelFrame class and has a scrollbar
# when using scrollFrame class the parent of chid widgets must be
# scrollFrame.frame and not scrollFrame

class ScrollFrame(ttk.LabelFrame):
    def __init__(self, parent, text=None, width: int = 0, height: int = 0, horizontal: bool = False):
        super().__init__(parent)

        if text != None:
            self.config(text=text)

        self.canvasWidget = Canvas(self)
        if width != 0:
            self.canvasWidget.config(width=width)

        if height != 0:
            self.canvasWidget.config(height=height)

        self.canvasVerticalScrollBar = ttk.Scrollbar(self, orient="vertical", command=self.canvasWidget.yview)
        self.canvasWidget.config(yscrollcommand=self.canvasVerticalScrollBar.set)

        self.canvasWidget.grid(row=0, column=0)
        self.canvasVerticalScrollBar.grid(row=0, column=1, sticky="NS")

        if horizontal == True:
            self.canvasHorizontalScrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.canvasWidget.xview)
            self.canvasWidget.config(xscrollcommand=self.canvasHorizontalScrollbar.set)
            self.canvasHorizontalScrollbar.grid(row=1, column=0, columnspan=2, sticky="EW")

        self.frame = ttk.Frame(self.canvasWidget)
        self.frame.grid(row=0, column=1)

        self.frame.bind("<Configure>",
                        lambda event: self.canvasWidget.config(scrollregion=self.canvasWidget.bbox("all")))

        self.canvasWidget.create_window((0, 0), window=self.frame)
