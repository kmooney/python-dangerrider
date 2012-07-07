import core
import datetime

class Sum(core.Aggregator):
    name = 'sum'
    value = 0
    
    def aggregate(self, val):
       self.value += val[0]   

class Average(core.Aggregator):
    name = 'average'
    value = 0
    count = 1
    
    def aggregate(self, val):
        self.value += val[0]
        self.value /= self.count
        self.count += 1

class Count(core.Aggregator):
    name = 'count'
    value = 0

    def aggregate(self, val):
        self.value += 1


class NumericIndex(core.RangeIndex):
    pass


class DateIndex(core.RangeIndex):
    """
        Date index will work on date ranges. It must
        index on only *one* property, because it is 
        a range index.  By default, the property is 
        'date', but this can be overriden.
    """
    properties = ['date']

    def update(self, obj):
        index_values = obj.get_index_values( self )

        if len(index_values) > 1: 
            raise Exception("RangeIndex must use just one property field")

        if type(index_values[0]) != datetime.datetime:
            raise TypeError("DateIndex Requires datetime.datetime values, got %s "%type(index_values[0]))
        super(DateIndex, self).update(obj)

    
        

    
