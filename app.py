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

# with app.app_context():
#     cyberminer.seed()

@app.route("/", methods=["GET"])
def index():
    return render_template(
        "cyberminer_index.html",
        results=[],
        keyword_mode="OR",
        sort_mode="url",
        page_num=0,
        items_per_page="5",
        filter_special_chars=None
    )

@app.route("/search/<int:page_num>", methods=["POST"])
def input_text(page_num=1):
    keywords = request.form["keywords"].split()
    keyword_mode = request.form["keyword-mode"]
    sort_mode = request.form["sort-mode"]

    items_per_page = request.form["items-per-page"]

    filter_special_chars = request.form.get("filter-special-chars")

    results = cyberminer.search(keywords, keyword_mode, sort_mode, page_num, int(items_per_page), True if filter_special_chars else False)

    return render_template(
        "cyberminer_index.html",
        results=results,
        search_text=request.form["keywords"],
        keyword_mode=keyword_mode,
        sort_mode=sort_mode,
        page_num=page_num,
        items_per_page=items_per_page,
        filter_special_chars=filter_special_chars
    )

@app.route("/visit", methods=["POST"])
def visit_website():
    data = request.json
    return {"url": cyberminer.visit(data["websiteId"])}

@app.route("/admin", methods=["GET"])
def admin(website=None):
    kwic_entries = cyberminer.getAllKwic()
    return render_template(
        "cyberminer_admin.html",
        kwic_entries = kwic_entries,
        added_website = website
    )

@app.route("/add-new-website", methods=["POST"])
def add_new_website():
    url = request.form["url"]
    desc = request.form["desc"]
    sponsor_money = float(request.form["sponsorMoney"])

    website = cyberminer.add_website(url, desc, sponsor_money)

    return admin(website)

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
