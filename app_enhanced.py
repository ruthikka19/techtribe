from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
from datetime import datetime, timedelta
import json

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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT UNIQUE,
        limit REAL,
        month TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS savings_goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        goal_name TEXT,
        target_amount REAL,
        current_amount REAL DEFAULT 0,
        deadline TEXT
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

    # Get date range filters
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    category_filter = request.args.get('category', '')

    # Base query
    expense_query = "SELECT * FROM expenses WHERE 1=1"
    params = []

    if start_date:
        expense_query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        expense_query += " AND date <= ?"
        params.append(end_date)
    if category_filter:
        expense_query += " AND category = ?"
        params.append(category_filter)

    cursor.execute(expense_query, params)
    expenses = cursor.fetchall()

    # Get all categories
    cursor.execute("SELECT DISTINCT category FROM expenses ORDER BY category")
    categories = [row[0] for row in cursor.fetchall()] if cursor.fetchall() else []
    cursor.execute("SELECT DISTINCT category FROM expenses ORDER BY category")
    categories = [row[0] for row in cursor.fetchall()]

    # Total expense
    total_query = "SELECT SUM(amount) FROM expenses WHERE 1=1"
    total_params = params.copy()
    
    if start_date or end_date or category_filter:
        cursor.execute(total_query + (" AND date >= ?" if start_date else "") + (" AND date <= ?" if end_date else "") + (" AND category = ?" if category_filter else ""), total_params)
    else:
        cursor.execute("SELECT SUM(amount) FROM expenses")
    total_expense = cursor.fetchone()[0] or 0

    # Total income
    cursor.execute("SELECT SUM(amount) FROM income")
    total_income = cursor.fetchone()[0] or 0

    # Category breakdown
    cursor.execute("SELECT category, SUM(amount) as total FROM expenses GROUP BY category ORDER BY total DESC")
    category_breakdown = cursor.fetchall()

    savings = total_income - total_expense

    conn.close()

    return render_template(
        "dashboard.html",
        expenses=expenses,
        total_expense=total_expense,
        total_income=total_income,
        savings=savings,
        categories=categories,
        category_breakdown=category_breakdown,
        start_date=start_date,
        end_date=end_date
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

@app.route("/delete_expense/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    return redirect("/")

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

@app.route("/delete_income/<int:income_id>", methods=["POST"])
def delete_income(income_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM income WHERE id = ?", (income_id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/set_budget", methods=["GET", "POST"])
def set_budget():
    if request.method == "POST":
        category = request.form["category"]
        limit = request.form["limit"]
        month = request.form["month"]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO budgets (category, limit, month) VALUES (?, ?, ?)",
            (category, limit, month)
        )
        conn.commit()
        conn.close()

        return redirect("/budgets")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM expenses")
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()

    return render_template("set_budget.html", categories=categories)

@app.route("/budgets")
def view_budgets():
    conn = connect_db()
    cursor = conn.cursor()

    current_month = datetime.now().strftime("%Y-%m")

    cursor.execute("SELECT * FROM budgets WHERE month = ?", (current_month,))
    budgets = cursor.fetchall()

    budget_data = []
    for budget in budgets:
        cursor.execute(
            "SELECT SUM(amount) FROM expenses WHERE category = ? AND strftime('%Y-%m', date) = ?",
            (budget['category'], current_month)
        )
        spent = cursor.fetchone()[0] or 0
        budget_data.append({
            'category': budget['category'],
            'limit': budget['limit'],
            'spent': spent,
            'remaining': budget['limit'] - spent,
            'percentage': (spent / budget['limit'] * 100) if budget['limit'] > 0 else 0
        })

    conn.close()
    return render_template("budgets.html", budget_data=budget_data)

@app.route("/api/chart_data")
def chart_data():
    conn = connect_db()
    cursor = conn.cursor()

    # Category pie chart
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    category_data = cursor.fetchall()

    # Monthly trend
    cursor.execute(
        "SELECT strftime('%Y-%m', date) as month, SUM(amount) FROM expenses GROUP BY month ORDER BY month"
    )
    monthly_data = cursor.fetchall()

    # Income vs Expense
    cursor.execute("SELECT SUM(amount) FROM income")
    total_income = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total_expense = cursor.fetchone()[0] or 0

    conn.close()

    return jsonify({
        'categories': [row[0] for row in category_data],
        'category_amounts': [row[1] for row in category_data],
        'months': [row[0] for row in monthly_data],
        'monthly_amounts': [row[1] for row in monthly_data],
        'income': total_income,
        'expense': total_expense
    })

@app.route("/savings_goals", methods=["GET", "POST"])
def savings_goals():
    if request.method == "POST":
        goal_name = request.form["goal_name"]
        target_amount = request.form["target_amount"]
        deadline = request.form["deadline"]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO savings_goals (goal_name, target_amount, deadline) VALUES (?, ?, ?)",
            (goal_name, target_amount, deadline)
        )
        conn.commit()
        conn.close()

        return redirect("/savings_goals")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM savings_goals")
    goals = cursor.fetchall()
    conn.close()

    return render_template("savings_goals.html", goals=goals)

@app.route("/reports")
def reports():
    conn = connect_db()
    cursor = conn.cursor()

    current_month = datetime.now().strftime("%Y-%m")

    # Monthly summary
    cursor.execute(
        "SELECT strftime('%Y-%m', date) as month, SUM(amount) as total FROM expenses GROUP BY month ORDER BY month DESC LIMIT 12"
    )
    monthly_summary = cursor.fetchall()

    # Current month details
    cursor.execute(
        "SELECT category, SUM(amount) FROM expenses WHERE strftime('%Y-%m', date) = ? GROUP BY category",
        (current_month,)
    )
    current_month_breakdown = cursor.fetchall()

    conn.close()

    return render_template("reports.html", monthly_summary=monthly_summary, current_month_breakdown=current_month_breakdown)

if __name__ == "__main__":
    create_tables()
    app.run(host="0.0.0.0", port=5000, debug=False)
