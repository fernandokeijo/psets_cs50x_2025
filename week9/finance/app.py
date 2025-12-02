import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""

    if request.method == "POST":
        moreCash = request.form.get("cash")

        try:
            moreCash = float(moreCash)
        except:
            return apology("Invalid value")

        if moreCash < 1:
            return apology("you cant add negative cash")

        cash = db.execute("SELECT cash FROM users WHERE id = ?;", session["user_id"])[0]["cash"]

        currentcash = cash + moreCash

        db.execute("UPDATE users SET cash = ? WHERE id = ?;", currentcash, session["user_id"])

        return redirect("/")



    stocksFromUser = db.execute("SELECT symbol, shares, price FROM purchases WHERE user_id = ?;", session["user_id"])

    yrcache = db.execute("SELECT cash FROM users WHERE id = ?;", session["user_id"])[0]["cash"]

    total = 0

    for stock in stocksFromUser:
        total += (stock["price"] * stock["shares"])





    return render_template("index.html", stocks = stocksFromUser, yrCache = yrcache, total = total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    ## gets only the current cash that the user has
    budget = db.execute("SELECT cash FROM users WHERE id = ?;" , session["user_id"])[0]["cash"]

    if request.method == "POST":

        stock = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        purchase = lookup(stock)

        check = db.execute("SELECT shares FROM purchases WHERE symbol = ? AND user_id = ?;", stock, session["user_id"])


        if not purchase:
            return apology("Invalid Stock symbol")

        if shares < 1:
            return apology("You can not buy a negative number of shares")

        if purchase["price"] * shares > budget:
            return apology("You don't have enough budget to purchase that amount of shares")

        if len(check) >= 1:
            currentShares = check[0]["shares"]
            currentTotal = currentShares + shares
            db.execute("UPDATE purchases SET shares = ? WHERE symbol = ? AND user_id = ?;", currentTotal, stock, session["user_id"])

        else:
            ## create tables
            db.execute("""
               CREATE TABLE IF NOT EXISTS purchases (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER NOT NULL,
               symbol TEXT NOT NULL,
               shares INTEGER NOT NULL,
               price NUMERIC NOT NULL,
               timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
               FOREIGN KEY (user_id) REFERENCES users(id)
               );

               """)

            db.execute("CREATE INDEX IF NOT EXISTS idx_purchases_user_id ON purchases(user_id)")
            db.execute("CREATE INDEX IF NOT EXISTS idx_purchases_symbol ON purchases(symbol)")



            db.execute("INSERT INTO purchases (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", session["user_id"], stock, shares, purchase["price"])
            new_budget = budget - purchase["price"] * shares
            db.execute("UPDATE users SET cash = ? WHERE id = ?", new_budget, session["user_id"])

            return redirect("/")



    return render_template("buy.html", budget = budget)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    history = db.execute("""
        SELECT symbol, shares, price, timestamp
        FROM purchases
        WHERE user_id = ?
        ORDER BY timestamp DESC;
    """, session["user_id"])




    return render_template("history.html", history = history)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        symbol = request.form.get("symbol")

        values = lookup(symbol)

        if not values:
            return apology("Invalid Symbol")

        return render_template("quoted.html", values= values)




    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        user = request.form.get("user")
        passwd = request.form.get("passwd")
        cpasswd = request.form.get("cpasswd")

        if not user or not passwd or not cpasswd:
            return apology("Fill the spaces in blank")
        elif passwd != cpasswd:
            return apology("passwords dont match")

        hashpasswd = generate_password_hash(passwd, method='scrypt', salt_length=16)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", user, hashpasswd)


        return redirect("/register")


    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":

        stock = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        stockValidation = lookup(stock)

        cash = db.execute("SELECT cash FROM users WHERE id = ?;" , session["user_id"])[0]["cash"]

        if not stockValidation:
            return apology("Invalid Stock symbol")

        if shares < 1:
            return apology("You can not sell a negative number of shares")


        rows = db.execute("SELECT shares FROM purchases WHERE symbol = ? AND user_id = ?;", stock, session["user_id"] )

        if len(rows) == 0:
            countShares = 0
        else:
            countShares = rows[0]["shares"]


        if countShares < shares:
            return apology("You can not sell more shares than you actually have")
        elif countShares == shares:

            db.execute("DELETE FROM purchases WHERE symbol = ? AND user_id = ?;", stock, session["user_id"])
            moneyUGot = stockValidation["price"] * shares
            newcash = cash + moneyUGot

            db.execute("UPDATE users SET cash = ? WHERE id = ?;", newcash, session["user_id"])

            redirect("/")
        else:
            newShares = countShares - shares

            db.execute("UPDATE purchases SET shares = ? WHERE symbol = ? AND user_id = ?;", newShares, stock, session["user_id"])
            moneyUGot = stockValidation["price"] * shares
            newcash = cash + moneyUGot

            db.execute("UPDATE users SET cash = ? WHERE id = ?", newcash, session["user_id"])

            redirect("/")

    return render_template("sell.html")
