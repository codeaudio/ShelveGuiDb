from tkinter import Button, Tk, Entry

from accessify import private

from peoplegui.gui.database.database import DataBase


class DeleteFrame(DataBase):
    def __init__(self, entries, master):
        self.entries = entries
        self.parent_master = master

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
        self._db.clear()
        self.close_shelve()
        self.counter(self.parent_master)
        self.master.destroy()
