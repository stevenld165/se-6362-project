# Takes strings and splits them by newline characters
# Stores these in its storage array
# Stores them as [[word, word2], [word, word2, word3]] pre-split
class LineStorage:
    def __init__(self):
        self.lines = []
    def add_lines(self, text):
        self.lines += [line.strip().split() for line in text.splitlines() if line.strip()]
    def get_line(self, index):
        return self.lines[index]
    def get_all(self):
        return [" ".join(line) for line in self.lines]
    def count(self):
        return len(self.lines)
    def reset(self):
        self.lines = []

FILLER_WORDS = ['a', 'the', 'is', 'in', 'on', 'and', 'to']

# Circular shifts must be done incrementally for each line.
# perhaps update this to use a hashmap of some sort to store the line information if needed
# also potentially update to be case insensitive
class CircularShift:
    def __init__(self, line_storage: LineStorage):
        self.line_storage = line_storage
        self.shifts = {}
        self.current_line_index = 0
    # Shifts the next line in LineStorage, and return the shifts for that line only
    def shift_next_line(self):
        if self.current_line_index >= self.line_storage.count():
            return []
        
        words = self.line_storage.get_line(self.current_line_index)
        self.shifts[self.current_line_index] = []
        line_shifts = []
        for i in range(len(words)):
            if (words[i].lower() not in FILLER_WORDS):
                shifted = words[i:] + words[:i]
                line_shifts.append(shifted)
                self.shifts[self.current_line_index].append(shifted)
            
        self.current_line_index += 1
        return [{"first_word": shift[0], "full_circular_shift": " ".join(shift)} for shift in line_shifts]
    def get_all_shifts(self):
        return self.shifts
    def reset(self):
        self.shifts = {}
        self.current_line_index = 0

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

class Kwic:
    def __init__(self):
        self.line_storage = LineStorage()
        self.circular_shift = CircularShift(self.line_storage)
        self.alphabetizer = Alphabetizer(self.circular_shift)
    def addWebsite(self, desc: str):
        # sanitize by removing everything after \n... or edit logic to ignore \n characters
        self.line_storage.add_lines(desc)
        shifts = self.circular_shift.shift_next_line()
        self.alphabetizer.alphabetize()

        return shifts
    def getAlphabetized(self):
        return self.alphabetizer.get_all()
    def reset(self):
        self.line_storage.reset()
        self.alphabetizer.reset()
        self.circular_shift.reset()
    

    

    
    