import random

class Variable(object):
    def __init__(self, name, domain, position=None):
        """Variable
        name a string
        domain a list of printable values
        position of form (x,y)
        """
        self.name = name # string
        self.domain = domain # list of values
        self.position = position if position else (random.random(), random.random())
        self.size = len(domain)
        self.index = 0

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __iter__(self):
        # The __iter__ method should return an iterator object,
        # which, in this case, is the instance itself (self).
        return self