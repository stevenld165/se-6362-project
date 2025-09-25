from flask import Flask, request, render_template_string

from kwic.Alphabetizer import Alphabetizer
from kwic.CircularShift import CircularShift
from kwic.LineStorage import LineStorage

app = Flask(__name__)

storage = LineStorage()
cs = CircularShift(storage)
alphabetizer = Alphabetizer(cs)

current_shifts = []

HTML = """
<!doctype html>
<title>KWIC Demo</title>
<h2>KWIC</h2>
<form method="post" action="/input">
  <textarea name="text" rows="6" cols="50"></textarea><br>
  <button type="submit">Store Input</button>
</form>

<hr>
<form method="post" action="/shift">
  <button type="submit">Generate Shifts for Next Line</button>
</form>

<form method="post" action="/alphabetize">
  <button type="submit">Alphabetize All Shifts</button>
</form>

<hr>

{% set colors = ["red", "blue", "green", "purple", "pink", "orange", "magenta"] %}

<h3>Line Storage:</h3>
<div>
{% for line in lines %}
    <p style="color: {{ colors[loop.index0 % colors|length] }}">{{ line }}</p>
{% endfor %}
</div>

<h3>Circular Shifts:</h3>
<div>
{% for line_group in shifts %}
    <div style="color: {{ colors[loop.index0 % colors|length] }}">
        {% for shift in line_group %}
            <p>{{ shift }}</p>
        {% endfor %}
    </div>
{% endfor %}
</div>

<h3>Alphabetized Shifts:</h3>
<div>
{% for alphabetized_shift in alphabetized_shifts %}
    <p>{{ alphabetized_shift }}</p>
{% endfor %}
</div>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(
        HTML,
        lines=storage.get_all(),
        shifts=current_shifts,
        alphabetized_shifts=alphabetizer.get_all()
    )

@app.route("/input", methods=["POST"])
def input_text():
    storage.reset()

    text = request.form["text"]
    storage.set_lines(text)

    alphabetizer.reset()
    cs.reset()
    current_shifts.clear()
    return index()

@app.route("/shift", methods=["POST"])
def shift_next():
    current_shifts.append(cs.shift_next_line())
    print(current_shifts)
    return index()

@app.route("/alphabetize", methods=["POST"])
def alphabetize_current():
    alphabetizer.alphabetize()
    return index()
