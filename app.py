from flask import Flask, request, render_template_string, render_template

from kwic.Alphabetizer import Alphabetizer
from kwic.CircularShift import CircularShift
from kwic.LineStorage import LineStorage
from kwic.cyberminer import Cyberminer

from database import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cyberminer.db"

db.init_app(app)

with app.app_context():
    db.create_all()

storage = LineStorage()
cs = CircularShift(storage)
alphabetizer = Alphabetizer(cs)

current_shifts = [] # this should be refactored to no longer use this i think the architecture supports it

# Cyberminer new code
cyberminer = Cyberminer()

@app.route("/", methods=["GET"])
def index():
    return render_template(
        "cyberminer_index.html",
        results=[],
        keyword_mode="OR",
        sort_mode="url",
        page_num=0,
        items_per_page="5",
    )

@app.route("/search/<int:page_num>", methods=["POST"])
def input_text(page_num=1):
    keywords = request.form["keywords"].split()
    keyword_mode = request.form["keyword-mode"]
    sort_mode = request.form["sort-mode"]

    items_per_page = request.form["items-per-page"]

    results = cyberminer.search(keywords, keyword_mode, sort_mode, page_num, int(items_per_page))

    return render_template(
        "cyberminer_index.html",
        results=results,
        search_text=request.form["keywords"],
        keyword_mode=keyword_mode,
        sort_mode=sort_mode,
        page_num=page_num,
        items_per_page=items_per_page
    )

@app.route("/visit", methods=["POST"])
def visit_website():
    data = request.json
    return {"url": cyberminer.visit(data["websiteId"])}


# @app.route("/", methods=["GET"])
# def index():
#     return render_template(
#         "kwic.html",
#         lines=storage.get_all(),
#         shifts=cs.get_all_shifts(),
#         alphabetized_shifts=alphabetizer.get_all()
#     )

# @app.route("/input", methods=["POST"])
# def input_text():
#     text = request.form["text"]
#     storage.set_lines(text)
#     return index()

# @app.route("/reset", methods=["POST"])
# def reset():
#     storage.reset()
#     alphabetizer.reset()
#     cs.reset()
#     current_shifts.clear()
#     return index()

# @app.route("/shift", methods=["POST"])
# def shift_next():
#     current_shifts.append(cs.shift_next_line())
#     alphabetizer.alphabetize()
#     print(current_shifts)
#     print(cs.get_all_shifts())
#     return index()

# @app.route("/alphabetize", methods=["POST"])
# def alphabetize_current():
#     alphabetizer.alphabetize()
#     return index()
