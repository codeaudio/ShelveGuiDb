from tkinter import Button, Tk, Entry

from accessify import private
from database import DataBase


class DeleteFrame(DataBase):
    def __init__(self, entries):
        self.entries = entries

    @private
    def __accept_buttons(self):
        Button(self.master.delete, text="Yes", command=self._accept_delete).grid(row=3, column=0)
        Button(self.master.delete, text="No", command=self.master.destroy).grid(row=3, column=4)

    def delete_all(self):
        self.master = Tk()
        self.master.title("delete all")
        self.master.delete = Entry(self.master, width=100)
        self.master.delete.pack()
        self.__accept_buttons()

    def _accept_delete(self):
        self.open_shelve(self.shelvename)
        for key in self._db.keys():
            del self._db[key]
        self.close_shelve()
        self.master.destroy()
