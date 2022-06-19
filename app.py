from audioop import add
from distutils.command.sdist import sdist
from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required

app = Flask(__name__)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///database.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    #POST
    if request.method == "POST":
        #Validate form submission
        if not request.form.get("username"):
            return apology("missing username")
        elif not request.form.get("password"):
            return apology("missing password")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match")

        #Add user to users database
        try:
            id = db.execute("INSERT INTO users (username, hash) VALUES (?,?)", request.form.get("username"), generate_password_hash(request.form.get("password")))
        except ValueError:
            return apology("username taken")

        #Log user in right away
        session["user_id"] = id

        #Redirec to main page
        return redirect("/")

    #GET
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    user = session["user_id"]
    selected_list = []
    if request.method == "POST":
        selected_form = request.form
        for s in selected_form:
            selected_list.append(s)
        # Delete
        if selected_list[-1] == "delete":
            for s in selected_list:
                db.execute("DELETE FROM selling WHERE id = ?", s)
            return redirect("/")
        # Submit
        elif selected_list[-1] == "submit":
            selections = selected_list[:-1]
            selections_info = []
            for s in selections:
                selections_info.append(db.execute("SELECT * FROM selling WHERE id = ?", s)[0])
            all_data = db.execute("SELECT * FROM selling WHERE user = ?", user)
            print(selections_info)
            return render_template("index.html", data = all_data, selections = selections_info, sendtext = True)
        else:
            return redirect("/")
    else:
        sd = db.execute("SELECT * FROM selling WHERE user = ?", user)
        return render_template("index.html", data = sd, sendtext = False)

@app.route("/input", methods=["GET", "POST"])
@login_required
def input():
    if request.method == "POST":
        favorite = 0
        selected = 0
        sell_type = request.form.get("sell_type")
        building_type = request.form.get("building_type")
        if building_type == "그 외":
            building_type = request.form.get("other-input")
        address = request.form.get("address")
        price = request.form.get("price")
        price_2 = request.form.get("price_2")
        rooms = request.form.get("rooms")
        use = request.form.get("use")
        loan = request.form.get("loan")
        parking = request.form.get("parking")
        date = request.form.get("date")
        phone_number = request.form.get("phone_number")
        comments = request.form.get("comments")
        user = session["user_id"]
        db.execute("INSERT INTO selling (favorite, selected, sell_type, building_type, address, price, price_2, rooms, use, loan, parking, date, phone_number, comments, user) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", favorite, selected, sell_type, building_type, address, price, price_2, rooms, use, loan, parking, date, phone_number, comments, user)
        return redirect("/")
    else:
        return render_template("input.html")
