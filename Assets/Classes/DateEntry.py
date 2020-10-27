from datetime import date
from tkinter import ttk, StringVar


class DateEntry(ttk.Frame):
    monthDict = {"January": 1, "February": 2, "March": 3, "April": 4,
                 "May": 5, "June": 6, "July": 7, "August": 8,
                 "September": 9, "October": 10, "November": 11, "December": 12}

    def __init__(self, parent):
        super().__init__(parent)

        self.yearEntry = ttk.Entry(self, width=6, justify="center")
        self.yearEntry.insert(0, "Year")
        self.yearEntry.bind("<Button-1>", lambda event: self.yearEntry.delete(0, "end"))

        self.monthStringVar = StringVar()
        self.monthStringVar.set("Month")
        self.monthOptionMenu = ttk.OptionMenu(self, self.monthStringVar, "Month", *list(self.monthDict.keys()))

        self.dayEntry = ttk.Entry(self, width=4, justify="center")

        self.yearEntry.grid(row=0, column=0)
        ttk.Label(self, text='/').grid(row=0, column=1)
        self.monthOptionMenu.grid(row=0, column=2)
        ttk.Label(self, text="/").grid(row=0, column=3)
        self.dayEntry.grid(row=0, column=4)

    def get(self) -> date:
        month = self.monthStringVar.get()
        if month == "Month":
            return
        else:
            month = self.monthDict[month]

        year = self.yearEntry.get()
        day = self.dayEntry.get()

        try:
            year = int(year)
            day = int(day)
        except ValueError:
            return None

        try:
            dateObj = date(year, month, day)
        except ValueError:
            return None

        return dateObj

    def set(self, date_obj: date):
        self.yearEntry.delete(0, "end")
        self.yearEntry.insert(0, date_obj.year)

        self.monthStringVar.set(list(self.monthDict.keys())[list(self.monthDict.values()).index(date_obj.month)])

        self.dayEntry.delete(0, "end")
        self.dayEntry.insert(0, date_obj.day)
