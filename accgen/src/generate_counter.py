class GenerateCounter:
    _generated = 0

    @classmethod
    def increase_generated(cls):
        cls._generated += 1
    
    @classmethod
    def get_generated(cls):
        return cls._generated

generate_counter = GenerateCounter()