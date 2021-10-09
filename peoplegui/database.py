import shelve

from accessify import protected


class DataBase:
    shelvename = 'class-shelve'
    fieldnames = ('name', 'age', 'job', 'pay')

    @protected
    def open_shelve(self, shelvename):
        self._db = shelve.open(shelvename)

    @protected
    def close_shelve(self):
        self._db.close()
