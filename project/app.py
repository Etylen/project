from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///list.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # Для вибраної групи створюємо журнал
        grup = request.form.get("grup")
        material = db.execute("SELECT number, name FROM list WHERE grup=?", grup)

        return render_template("F_EN_SH.htm", grup_number = grup, material=material)

    else:

        # Display the entries in the database on index.html COUNT
        list = db.execute("SELECT * FROM list")

        #Визначаємо скільки студентів в БД
        number_of_students = db.execute("SELECT MAX(id) FROM list")
        nos = number_of_students[0]["MAX(id)"]

        #Визначаємо максимальну кількість студентів в групі
        max_students = db.execute("SELECT MAX(number) FROM list")
        ms = max_students[0]["MAX(number)"]

        #Визначаємо кількість груп
        all_groups = db.execute("SELECT COUNT(DISTINCT grup) FROM list")
        ag = all_groups[0]["COUNT(DISTINCT grup)"]

        #Визначаємо і передаємо номери груп
        groups = db.execute("SELECT DISTINCT grup FROM list")
        gr = [row["grup"] for row in groups]

        return render_template("index.html", list=list, number_of_students = nos, max_students = ms, all_groups=ag, groups=gr)


#@app.route("/empty", methods=["GET"])
#def empty():
#    return render_template("empty.html")