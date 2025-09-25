from kwic import CircularShift

class Alphabetizer:
    def __init__(self, circular_shift : CircularShift):
        self.circular_shift = circular_shift
        self.alphabetized_shifts = []
    def alphabetize(self):
        self.alphabetized_shifts = sorted(self.circular_shift.get_all_shifts())
        return self.alphabetized_shifts[:]
    def get_all(self):
        return [" ".join(shift) for shift in self.alphabetized_shifts]
    def reset(self):
        self.alphabetized_shifts = []
    