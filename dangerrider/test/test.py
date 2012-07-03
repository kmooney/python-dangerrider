import core

class Sum(core.Aggregator):
    properties = []
    value = 0
    name = 'Sum'

    def aggregate(self, val):
        self.value += val[0]

class Average(core.Aggregator):
    properties = []
    value = 0
    count = 1
    
    def aggregate(self, val):
        self.value += val[0] 
        self.value /= self.count
        self.count += 1

class AverageAge(Average):
    properties = ['age']

class TotalAge(Sum):
    properties = ['age']

class NameIndex(core.Index):
    properties = ['name']
    name = "Name Index"
    
class BasePerson(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Person(BasePerson, core.StorageMixin):
    pass

table = core.Table()

table.aggregators=[AverageAge(), TotalAge()]

table.add_index(NameIndex())

person = Person('Kevin', 32)
person2 = Person('Sarah', 26)

table.add_object(person)
table.add_object(person2)
print "Person is %s" %person
print "Person2 is %s" %person
print "Average Age: %s" %table.aggregators[0].value
print "Total Age: %s" %table.aggregators[1].value

ret_person = table.filter(('name',),('Kevin',))
print "We got %s from query" %ret_person
