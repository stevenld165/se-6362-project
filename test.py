from kwic.CircularShift import CircularShift
from kwic.LineStorage import LineStorage
from kwic.Alphabetizer import Alphabetizer

storage = LineStorage()
cs = CircularShift(storage)
alphabetizer = Alphabetizer(cs)

storage.set_lines("This is a test\nBeauty and the beast\nMeow woof quack baaaa meow purr growl\nword")

for line in storage.get_all():
    print(cs.shift_next_line())

print ("Alphabetizing!")

print(alphabetizer.alphabetize())

