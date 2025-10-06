from kwic import LineStorage

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
        return [" ".join(shift) for shift in line_shifts]
    def get_all_shifts(self):
        return self.shifts
    def reset(self):
        self.shifts = {}
        self.current_line_index = 0
        