class Language:
    def __init__(self, iso, data):
        self.iso = iso
        self.data = data
        self.total_frequencies = 0
        self.conditional_probabilities = {}

