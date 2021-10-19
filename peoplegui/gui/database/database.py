import shelve
from tkinter import Message


class DataBase:
    shelvename = 'class-shelve'
    fieldnames = ('name', 'age', 'job', 'pay', 'residence')

    def open_shelve(self, shelvename):
        self._db = shelve.open(shelvename)

    def close_shelve(self):
        self._db.close()

    def counter(self, master):
        self.open_shelve(self.shelvename)
        Message(master, text=f'rec-{len(self._db.keys())}').grid(row=5, column=3)
        self.close_shelve()
