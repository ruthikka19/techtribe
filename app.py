from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        category TEXT,
        date TEXT,
        description TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS income (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        amount REAL,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

def connect_db():
    conn = sqlite3.connect("database.db", timeout=5)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def dashboard():
    conn = connect_db()
    cursor = conn.cursor()

    # Get all expenses
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    # Total expense
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total_expense = cursor.fetchone()[0] or 0

    # Total income
    cursor.execute("SELECT SUM(amount) FROM income")
    total_income = cursor.fetchone()[0] or 0

    savings = total_income - total_expense

    conn.close()

    return render_template(
        "dashboard.html",
        expenses=expenses,
        total_expense=total_expense,
        total_income=total_income,
        savings=savings
    )


@app.route("/add_expense", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        amount = request.form["amount"]
        category = request.form["category"]
        date = request.form["date"]
        description = request.form["description"]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?)",
            (amount, category, date, description)
        )
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add_expense.html")
@app.route("/add_income", methods=["GET", "POST"])
def add_income():
    if request.method == "POST":
        source = request.form["source"]
        amount = request.form["amount"]
        date = request.form["date"]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO income (source, amount, date) VALUES (?, ?, ?)",
            (source, amount, date)
        )
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add_income.html")


if __name__ == "__main__":
    create_tables()
    app.run(host="0.0.0.0", port=5000, debug=False)

