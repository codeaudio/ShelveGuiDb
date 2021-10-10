class Person:
    def __init__(self, name, age, pay=0, job=None, residence=None):
        self.name = name
        self.age = age
        self.pay = pay
        self.job = job
        self.residence = residence

    def __str__(self):
        return f'{self.__class__.__name__, self.__dict__}'

    def last_name(self) -> str:
        return self.name.split()[-1]

    def give_raise(self, percent):
        self.pay = int(self.pay * (1.0 + percent))


if __name__ == '__main__':
    bob = Person('Bov Smith', 42, job='software')
    sue = Person('Sue Jones', 45, 40000, 'hardware')
    persons = [bob, sue]
    print(bob.name.split()[-1])
    sue.pay *= 1.5
    print(sue.pay)
    print([(el.name, el.pay) for el in persons if el.pay > 30000])
    sue.give_raise(.10)
    print(sue.pay)
