from flask import Flask, request, render_template_string, render_template

from kwic.Alphabetizer import Alphabetizer
from kwic.CircularShift import CircularShift
from kwic.LineStorage import LineStorage

app = Flask(__name__)

storage = LineStorage()
cs = CircularShift(storage)
alphabetizer = Alphabetizer(cs)

current_shifts = [] # this should be refactored to no longer use this i think the architecture supports it

@app.route("/", methods=["GET"])
def index():
    return render_template(
        "kwic.html",
        lines=storage.get_all(),
        shifts=cs.get_all_shifts(),
        alphabetized_shifts=alphabetizer.get_all()
    )

@app.route("/input", methods=["POST"])
def input_text():
    text = request.form["text"]
    storage.set_lines(text)
    return index()

@app.route("/reset", methods=["POST"])
def reset():
    storage.reset()
    alphabetizer.reset()
    cs.reset()
    current_shifts.clear()
    return index()

@app.route("/shift", methods=["POST"])
def shift_next():
    current_shifts.append(cs.shift_next_line())
    alphabetizer.alphabetize()
    print(current_shifts)
    print(cs.get_all_shifts())
    return index()

@app.route("/alphabetize", methods=["POST"])
def alphabetize_current():
    alphabetizer.alphabetize()
    return index()
