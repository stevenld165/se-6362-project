from kwic import CircularShift

class Alphabetizer:
    def __init__(self, circular_shift : CircularShift):
        self.circular_shift = circular_shift
        self.alphabetized_shifts = []
    def alphabetize(self):
        # currently doesn't do any smart merge sort kinda thing, im thinking store a set of indexes done, then merge it if not already included
        unsorted_shifts = [shift for group in self.circular_shift.get_all_shifts().values() for shift in group]
        self.alphabetized_shifts = sorted(unsorted_shifts)
        return self.alphabetized_shifts[:]
    def get_all(self):
        return [" ".join(shift) for shift in self.alphabetized_shifts]
    def reset(self):
        self.alphabetized_shifts = []
    