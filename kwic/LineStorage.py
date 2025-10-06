# Takes strings and splits them by newline characters
# Stores these in its storage array
# Stores them as [[word, word2], [word, word2, word3]] pre-split
class LineStorage:
    def __init__(self):
        self.lines = []
    def set_lines(self, text):
        self.lines += [line.strip().split() for line in text.splitlines() if line.strip()]
    def get_line(self, index):
        return self.lines[index]
    def get_all(self):
        return [" ".join(line) for line in self.lines]
    def count(self):
        return len(self.lines)
    def reset(self):
        self.lines = []