class Person:
    def __init__(self, name, age, pay=0, job=None):
        self.name = name
        self.age = age
        self.pay = pay
        self.job = job

    def __str__(self):
        return f'{self.__class__.__name__, self.__dict__}'

    def last_name(self) -> str:
        return self.name.split()[-1]
