import json
from tkinter import Entry, Tk, Button
from tkinter.messagebox import showerror

from peoplegui.gui.database.database import DataBase
from peoplegui.gui.validator.validator import Validator


class DataFrame(DataBase):
    update_key = None
    index = None

    def __init__(self, entries):
        self.entries = entries

    def get_data(self):
        self.open_shelve(self.shelvename)
        self.master = Tk()
        self.master.title("all data")
        for i, v in enumerate(self._db.items()):
            self.master.i = Entry(self.master, width=150)
            self.master.i.pack()
            self.entries[i] = self.master.i
            update = UpdateFrame()
            update.update_key, update.entries, update.index = v[0], self.entries[i], i
            self.entries[i].insert(
                i, ({v[0]: {field: str(getattr(v[1], field)) for field in self.fieldnames}},
                    Button(self.master, text="Update", command=update.update_record).pack())[0]
            )
        self.close_shelve()


class UpdateFrame(DataBase):
    update_key = None
    index = None
    entries = None
    validator = Validator.DictValidator()

    def update_record(self):
        self.open_shelve(self.shelvename)
        try:
            record = self._db[self.update_key]
            print(record)
        except Exception as e:
            showerror(title='error', message='not found')
            raise Exception(e)
        try:
            self.validator.entries = dict(
                json.loads(str(self.entries.get())
                           .replace("'", '"').replace('"{', '{').replace('}"', '}')
                           .replace('"[', '[').replace(']"', ']'))
            ).get(self.update_key)
        except Exception as e:
            showerror(title='error', message='incorrect data structure')
            raise Exception(e)
        for field in self.fieldnames:
            try:
                self.validator._field_empty_validator(self.update_key, field, ['name', 'job'])
                self.validator._field_integer_validator(self.update_key, field, ['age', 'pay'])
                setattr(record, field, self.validator.entries[field])
            except Exception as e:
                showerror(title='error', message='not found')
                raise Exception(e)
        self._db[self.update_key] = record
        self.close_shelve()
