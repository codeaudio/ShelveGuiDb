import random

from accessify import private, protected
import shelve
from tkinter import *
from tkinter.messagebox import showerror

from class_person.person_start import Person


class Validator:
    def __init__(self, entries):
        self.entries = entries

    @protected
    def _field_empty_validator(self, key, field):
        if str(key).strip() == '':
            showerror(title='error', message=f"'key' = {str(key) != ''} Empty field: 'field' = key")
            raise ValueError(f"'key' = {str(key) != ''} Empty field: 'field' = key")
        if str(self.entries[field].get()).strip() == '':
            showerror(title='error', message=f"'key' = {key} Empty field: {field}")
            raise ValueError(f"'key' = {key} Empty field: {field}")

    @protected
    def _field_integer_validator(self, key, field, validate_field: list):
        if field in validate_field and not str(self.entries[field].get()).strip().isdigit():
            showerror(title='error', message=f"is not a number: 'key' = {key}, 'field' = {field}")
            raise ValueError(f"is not a number: {key, field}")


class Gui(Frame, Validator):
    shelvename = 'class-shelve'
    fieldnames = ('name', 'age', 'job', 'pay')

    def __init__(self):
        super().__init__()
        self.master.title('gui')
        self.entries = {}

    @private
    def open_shelve(self, shelvename):
        self.__db = shelve.open(shelvename)

    @private
    def close_shelve(self):
        self.__db.close()

    def make_widgets(self):
        self.make_root_master_buttons()
        for (ix, label) in enumerate(('key',) + self.fieldnames):
            self.master.lab = Label(self.master, text=label)
            self.master.ent = Entry(self.master)
            self.master.lab.grid(row=ix, column=0)
            self.master.ent.grid(row=ix, column=1)
            self.entries[label] = self.master.ent
        return self.master.mainloop()

    def make_root_master_buttons(self):
        Button(self.master, text="Fetch", command=self.fetch_record).grid(row=5, column=0)
        Button(self.master, text="Update", command=self.update_record).grid(row=5, column=1)
        Button(self.master, text="Quit", command=self.master.quit).grid(row=5, column=2)
        Button(self.master, text="Delete", command=self.delete_record).grid(row=5, column=3)
        Button(self.master, text="Get data", command=self.get_data).grid(row=0, column=3)
        Button(self.master, text="Generate", command=self.generate).grid(row=1, column=3)
        Button(self.master, text="Clear", command=self.clear_fields).grid(row=2, column=3)
        Button(self.master, text="Delete all", command=self.delete_all).grid(row=3, column=3)

    def fetch_record(self):
        self.open_shelve(self.shelvename)
        key = self.entries['key'].get()
        try:
            record = self.__db[key]
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
        if key in self.__db:
            record = self.__db[key]
        else:
            record = Person(name='?', age='?')
        for field in self.fieldnames:
            self._field_empty_validator(key, field), self._field_integer_validator(key, field, ['age', 'pay'])
            setattr(record, field, str(self.entries[field].get()))
        self.__db[key] = record
        self.close_shelve()

    def delete_record(self):
        self.open_shelve(self.shelvename)
        key = self.entries['key'].get()
        if key in self.__db:
            del self.__db[key]
            self.clear_fields()
        self.close_shelve()

    def delete_all(self):
        self.master = Tk()
        self.master.title("delete all")
        self.master.d = Entry(self.master, width=100)
        self.master.d.pack()
        Button(self.master.d, text="Yes", command=self.accept_delete).grid(row=3, column=0)
        Button(self.master.d, text="No", command=self.master.destroy).grid(row=3, column=4)

    def accept_delete(self):
        self.open_shelve(self.shelvename)
        for key in self.__db.keys():
            del self.__db[key]
        self.close_shelve()
        self.master.destroy()

    def get_data(self):
        self.open_shelve(self.shelvename)
        self.master = Tk()
        self.master.title("all data")
        for i, v in enumerate(self.__db.items()):
            self.master.i = Entry(self.master, width=100)
            self.master.i.pack()
            self.entries[i] = self.master.i
            self.entries[i].insert(i, {v[0]: {field: str(getattr(v[1], field)) for field in self.fieldnames}})
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
