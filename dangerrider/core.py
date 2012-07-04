class Table(object):
    """
        A table is an indexed container that holds objects.  As long as the 
        indices are attached before the objects are added, then refresh_indices
        must be called.
    """
    object_list = []
    indices = {} 
    aggregators = {} 

    def refresh_indices(self):
        # clear all the indices
        for index in self.indices.itervalues():
            index.clear()

        # update all the indices, for each item
        for obj in self.object_list:
            self.update_indices(obj)

    def update_indices(self, obj):
        for index in self.indices.itervalues():
            index.update(obj)
        
    def add_object(self, obj):
        self.object_list.append(obj)

        self.update_indices(obj)

        for aggregator in self.aggregators:
            aggregator.update(obj)

    def add_index(self, index):
        self.indices[tuple(index.properties)] = index

    def add_aggregator(self, aggregator):
        self.aggregators[aggregator.name] = aggregator
    
    def get_query_info(self):
        return self.query_info

    def range(self, key_tuple, start, end=None):
        if key_tuple in self.indices:
            return self.indices[key_tuple].get_objects_by_range(start,end)
 
    def filter(self, key_tuple, value_tuple):
        self.query_info = {'key_tuple': key_tuple, 'value_tuple': value_tuple }
        if len(key_tuple) != len(value_tuple):
            raise Exception("Keys and Values must have the same cardinality!")
        # first, see if the values are in the index
        if key_tuple in self.indices:
            self.query_info['index'] = self.indices[key_tuple].name
            return self.indices[key_tuple].get_objects(value_tuple) 

        self.query_info['index'] = 'No Index (Search)'

        #if not, filter by key/value
        rvalue = [ ] 
        for obj in self.object_list:
            include = True
            for key, val in zip(key_tuple, value_tuple):
                if getattr(obj, key) != val:
                    include = False
                    break
            if include:
                rvalue.append(obj) 
            
    def metadata(self):
        return {'indices': self.indices, 
                'aggregators': self.aggregators,
                'last_query_info': self.query_info}        

    def __init__(self):
        self.object_list = []
        self.indices = {} 
        self.aggregators = []

class StorageMixin(object):
    """
        Use this mixin to make your objects compatible with the dangerrider table.
    """
    def get_index_values(self, index):
        return tuple([getattr(self,prop,None) for prop in index.properties])
        
class Index(object):
    """
        An index holds references to objects in the Table with a dictionary 
        that allows for quick lookup by tuple.
    """
    name = ''
    properties = [ ]
    lookup = { } 

    def __init__(self, name, properties = []):
        self.name = name
        if len(properties) > 0:
            self.properties = properties

    def update(self, obj):
        index_values = obj.get_index_values( self )
        if index_values not in self.lookup:
            self.lookup[index_values] = [] 
        self.lookup[index_values].append( obj )
    
    def set_properties(self, props):
        self.properties = props 

    def clear(self):
        self.lookup = { } 

    def get_objects(self, index_tuple):
        return self.lookup[index_tuple]

class RangeIndex(Index):
    """
        A range index refers to properties that fall within a range.  Range indexes
        can only index a single property (how to tell if a tuple is greater or less 
        than another?)  Range Indexes are not too useful for objects or words, but are
        super useful for numbers.  

        There are surely more complicated, faster ways to do this.
    """ 
    def set_properties(self, props):
        if len(props) > 1:
            raise Exception ("Range Index Must be on a single property")
        super(RangeIndex, self).set_properties(props)

    def update(self, obj):
        index_values = obj.get_index_values( self )
        if len(index_values) > 1:
            raise Exception ("Range Index Must be on a single value")
        super(RangeIndex, self).update(obj)

    def get_objects(self, index_tuple):
        if len(index_tuple) > 1:
            raise Exception ("Range Index Must be on a single value")
        return super(RangeIndex, self).get_objects(index_tuple)
    
    def get_objects_by_range(self, range_start, range_end=None):
        keys = sorted(list(self.lookup.iterkeys()))
        if range_end != None:
            return [a for b in [self.lookup[key] for key in keys if key >= (range_start,) and key <= (range_end,)] for a in b]
        else:
            return [a for b in [self.lookup[key] for key in keys if key >= (range_start,)] for a in b]
    
class Aggregator(object):
    """
        An aggregator contains precalculated values for things like sums, averages, 
        counts, etc.
    """
    name = ''
    properties = [ ]
    value = None
    
    def update(self, obj):
        self.aggregate(obj.get_index_values(self))

    def aggregate():
        return ''
