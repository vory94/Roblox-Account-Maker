class Counter:
    _counter = 0
    
    @classmethod
    def increment(cls):
        cls._counter += 1
    
    @classmethod
    def get_value(cls):
        return cls._counter

counter = Counter()