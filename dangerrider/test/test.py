import core
import unittest


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

class AgeIndex(core.RangeIndex):
    properties = ['age']
    
class BasePerson(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Person(BasePerson, core.StorageMixin):
    pass


class DangerTests(unittest.TestCase):
   
    def setUp(self):
        self.table = core.Table()
        self.table.aggregators=[AverageAge(), TotalAge()]
        self.table.add_index(NameIndex("NameIndex"))
        self.person = Person('Kevin', 32)
        self.person2 = Person('Sarah', 26)
        self.table.add_object(self.person)
        self.table.add_object(self.person2)
        

    def testAggregators(self):
        ret_person = self.table.filter(('name',),('Kevin',))
        self.assertEqual(ret_person[0], self.person)
        self.assertEqual(self.table.aggregators[0].value, 29)
        self.assertEqual(self.table.aggregators[1].value, 58)   

    def testRangeIndex(self):
        range_index = AgeIndex('AgeIndex')
        self.table.add_index(range_index)
        self.table.refresh_indices() 
        ret_person = self.table.filter(('age',),(32,))
        self.assertEqual(ret_person[0], self.person)

        ret_people = self.table.range(('age',), 8, 80)
        self.assertEqual(len(ret_people), 2)

        ret_people = self.table.range(('age',), 8, None)
        self.assertEqual(len(ret_people), 2)

        ret_people = self.table.range(('age',), 29, None)
        self.assertEqual(len(ret_people), 1)

        ret_people = self.table.range(('age',), 24, 29)
        self.assertEqual(len(ret_people), 1)
        self.assertEqual(ret_people[0], self.person2)

        ret_people = self.table.range(('age',), 29, 32)
        self.assertEqual(len(ret_people), 1)
        self.assertEqual(ret_people[0], self.person)
         
        

if __name__ == '__main__':
    unittest.main(verbosity=2)
