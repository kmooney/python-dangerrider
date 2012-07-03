class Table(object):
    object_list = []
    indices = {} 
    aggregators = [] 

    def add_object(self, obj):
        self.object_list.append(obj)

        for index in self.indices.iteritems():
            index.update(obj)

        for aggregator in self.aggregators:
            aggregator.update(obj)

    def add_index(self, index):
        self.indices[tuple(index.properties)] = index

    def filter(self, key_tuple, value_tuple):
        if len(key_tuple) != len(value_tuple):
            raise Exception("Keys and Values must have the same cardinality!")
        # first, see if the values are in the index
        if key_tuple in self.indices:
            return self.indices[key_tuple].get_objects(value_tuple) 

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
            
    def __init__(self):
        self.object_list = []
        self.indices = {} 
        self.aggregators = []

class StorageMixin(object):
    def get_index_values(self, index):
        return tuple([getattr(self,prop,None) for prop in index.properties])
        
class Index(object):
    name = ''
    properties = [ ]
    lookup = { } 

    def update(self, obj):
        index_values = obj.get_index_values( self )
        if index_values not in self.lookup:
            self.lookup = [ ]
        self.lookup[index_values].append( obj )

    def get_objects(self, index_tuple):
        return self.lookup(index_tuple)

class Aggregator(object):
    name = ''
    properties = [ ]
    value = None
    
    def update(self, obj):
        self.aggregate(obj.get_index_values(self))

    def aggregate():
        return ''
