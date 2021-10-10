import shelve


class DataBase:
    shelvename = 'class-shelve'
    fieldnames = ('name', 'age', 'job', 'pay', 'residence')

    def open_shelve(self, shelvename):
        self._db = shelve.open(shelvename)

    def close_shelve(self):
        self._db.close()
