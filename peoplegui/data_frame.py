from tkinter import Entry, Tk

from database import DataBase


class DataFrame(DataBase):

    def __init__(self, entries):
        self.entries = entries

    def get_data(self):
        self.open_shelve(self.shelvename)
        self.master = Tk()
        self.master.title("all data")
        for i, v in enumerate(self._db.items()):
            self.master.i = Entry(self.master, width=100)
            self.master.i.pack()
            self.entries[i] = self.master.i
            self.entries[i].insert(i, {v[0]: {field: str(getattr(v[1], field)) for field in self.fieldnames}})
        self.close_shelve()
