import core
import util
import unittest
import datetime


class AverageAge(util.Average):
    properties = ['age']

class TotalAge(util.Sum):
    properties = ['age']

class NameIndex(core.Index):
    properties = ['name']
    name = "Name Index"

class AgeIndex(core.RangeIndex):
    properties = ['age']
    
class BirthdayIndex(util.DateIndex):
    properties = ['birthday']

class BasePerson(object):
    def __init__(self, name, age, birthday):
        self.name = name
        self.age = age
        self.birthday = birthday

class Person(BasePerson, core.StorageMixin):
    pass


class DangerTests(unittest.TestCase):
   
    def setUp(self):
        self.table = core.Table()
        self.table.aggregators=[AverageAge(), TotalAge()]
        self.table.add_index(NameIndex("NameIndex"))
        self.person = Person('Kevin', 32, datetime.datetime(year=1979, month=11, day=26))
        self.person2 = Person('Sarah', 26, datetime.datetime(year=1985, month=12, day=26))
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

    def testDateIndex(self):
        birthday_index = BirthdayIndex("BirthdayIndex")
        self.table.add_index(birthday_index)
        # TODO ability to refresh just one index
        self.table.refresh_indices()
        ret_person = self.table.filter(('birthday',), (datetime.datetime(year=1979, month=11, day=26),))
        self.assertEqual(len(ret_person), 1)
        self.assertEqual(ret_person[0], self.person)
        ret_people = self.table.range(('birthday',), datetime.datetime(year=1979, month=1, day=1),
                                                     datetime.datetime(year=1979, month=12, day=31))

        self.assertEqual(len(ret_people), 1)
        self.assertEqual(ret_people[0], self.person)

        ret_people = self.table.range(('birthday',), datetime.datetime(year=1979, month=1, day=1),
                                                     datetime.datetime(year=1999, month=1, day=1))
        self.assertEqual(len(ret_people), 2)
        self.assertEqual(ret_people[0], self.person)
        self.assertEqual(ret_people[1], self.person2)
        


if __name__ == '__main__':
    unittest.main(verbosity=2)
