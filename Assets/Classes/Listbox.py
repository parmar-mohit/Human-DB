from tkinter import ttk


class Listbox(ttk.Frame):
    def __init__(self, parent, heading: str, height: int, width: int):
        super().__init__(parent)

        self.treeview = ttk.Treeview(self, selectmode="browse", height=height)
        self.treeview.column("#0", width=width)
        self.treeview.heading("#0", text=heading)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.treeview.yview)
        self.treeview.config(yscrollcommand=scrollbar.set)

        self.treeview.grid(row=0, column=0, padx=5, pady=5)
        scrollbar.grid(row=0, column=1, sticky="NS", padx=5, pady=5)

    def delete_all(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)

    def delete_selected(self):
        self.treeview.delete(self.treeview.focus())

    def get(self):
        return self.treeview.item(self.treeview.focus())

    def insert(self, text: str):
        self.treeview.insert(parent="", index="end", text=text)
