import random
from tkinter import *
from tkinter.messagebox import showerror

from accessify import private

from class_person.person_start import Person
from database.database import DataBase
from validator.validator import Validator
from widget_frame.data_frame import DataFrame
from widget_frame.delete_frame import DeleteFrame


class Gui(DataBase):
    def __init__(self):
        self.master = Frame().master
        self.master.title('gui')
        self.entries = {}
        self.validator = Validator.EntriesValidator()
        self.validator.entries = self.entries

    def make_widgets(self):
        self.make_root_master_buttons()
        for (ix, label) in enumerate(('key',) + self.fieldnames):
            self.master.lab = Label(self.master, text=label)
            self.master.ent = Entry(self.master)
            self.master.lab.grid(row=ix, column=0)
            self.master.ent.grid(row=ix, column=1)
            self.entries[label] = self.master.ent
        return self.master.mainloop()

    @private
    def make_root_master_buttons(self):
        Button(self.master, text="Fetch", command=self.fetch_record).grid(row=5, column=0)
        Button(self.master, text="Update", command=self.update_record).grid(row=5, column=1)
        Button(self.master, text="Quit", command=self.master.quit).grid(row=5, column=2)
        Button(self.master, text="Delete", command=self.delete_record).grid(row=5, column=3)
        Button(self.master, text="Get data", command=DataFrame(self.entries).get_data).grid(row=0, column=3)
        Button(self.master, text="Generate", command=self.generate).grid(row=1, column=3)
        Button(self.master, text="Delete all", command=DeleteFrame(self.entries).delete_all).grid(row=2, column=3)
        Button(self.master, text="Clear", command=self.clear_fields).grid(row=3, column=3)

    def fetch_record(self):
        self.open_shelve(self.shelvename)
        key = self.entries['key'].get()
        try:
            record = self._db[key]
        except KeyError:
            showerror(title='error', message='no such key')
        else:
            for field in self.fieldnames:
                self.entries[field].delete(0, END)
                self.entries[field].insert(0, getattr(record, field.strip()))
        self.close_shelve()

    def update_record(self):
        self.open_shelve(self.shelvename)
        key = self.entries['key'].get()
        if key in self._db:
            record = self._db[key]
        else:
            record = Person(name='?', age='?')
        for field in self.fieldnames:
            self.validator._field_empty_validator(key, field)
            self.validator._field_integer_validator(key, field, ['age', 'pay'])
            setattr(record, field, str(self.entries[field].get()))
        self._db[key] = record
        self.close_shelve()

    def delete_record(self):
        self.open_shelve(self.shelvename)
        key = self.entries['key'].get()
        if key in self._db:
            del self._db[key]
            self.clear_fields()
        self.close_shelve()

    def clear_fields(self):
        self.entries['key'].delete(0, END)
        for field in self.fieldnames:
            self.entries[field].delete(0, END)

    def generate(self):
        self.clear_fields()
        for field in self.fieldnames:
            self.entries['key'].insert(0, random.randint(0, 100))
            if field in ['name', 'job']:
                self.entries[field].insert(0, ''.join(random.choice('qwertyuiopasdfghjklzxcvbnm') for _ in range(12)))
            elif field == 'age':
                self.entries[field].insert(0, random.randint(0, 99))
            else:
                self.entries[field].insert(0, random.randint(0, 9999))


if __name__ == '__main__':
    Gui().make_widgets()
