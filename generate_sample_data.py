import sqlite3
from datetime import datetime, timedelta
import random

def connect_db():
    return sqlite3.connect("database.db")

def generate_sample_data():
    conn = connect_db()
    cursor = conn.cursor()

    # Sample expenses data
    expenses_data = [
        (500, "Food", "2024-01-05", "Grocery shopping"),
        (150, "Transport", "2024-01-08", "Taxi fare"),
        (2000, "Shopping", "2024-01-10", "Clothes"),
        (300, "Food", "2024-01-12", "Restaurant"),
        (100, "Entertainment", "2024-01-15", "Movie tickets"),
        (450, "Food", "2024-01-18", "Grocery shopping"),
        (200, "Transport", "2024-01-20", "Fuel"),
        (1500, "Shopping", "2024-01-22", "Electronics"),
        (250, "Food", "2024-01-25", "Restaurant"),
        (80, "Entertainment", "2024-01-28", "Gaming"),
        (600, "Food", "2024-02-02", "Grocery shopping"),
        (180, "Transport", "2024-02-05", "Taxi fare"),
        (1800, "Shopping", "2024-02-08", "Furniture"),
        (350, "Food", "2024-02-10", "Restaurant"),
        (120, "Entertainment", "2024-02-12", "Concert"),
        (500, "Food", "2024-02-15", "Grocery shopping"),
        (220, "Transport", "2024-02-18", "Bus pass"),
        (1200, "Shopping", "2024-02-20", "Shoes"),
        (280, "Food", "2024-02-22", "Restaurant"),
        (150, "Entertainment", "2024-02-25", "Streaming"),
        (550, "Food", "2024-03-02", "Grocery shopping"),
        (200, "Transport", "2024-03-05", "Taxi fare"),
        (2200, "Shopping", "2024-03-08", "Clothes"),
        (320, "Food", "2024-03-10", "Restaurant"),
        (100, "Entertainment", "2024-03-12", "Books"),
        (480, "Food", "2024-03-15", "Grocery shopping"),
        (190, "Transport", "2024-03-18", "Fuel"),
        (1600, "Shopping", "2024-03-20", "Accessories"),
        (290, "Food", "2024-03-22", "Restaurant"),
        (160, "Entertainment", "2024-03-25", "Sports"),
        (520, "Food", "2024-04-02", "Grocery shopping"),
        (210, "Transport", "2024-04-05", "Taxi fare"),
        (1900, "Shopping", "2024-04-08", "Gadgets"),
        (330, "Food", "2024-04-10", "Restaurant"),
    ]

    # Sample income data
    income_data = [
        (25000, "Salary", "2024-01-01"),
        (5000, "Freelance", "2024-01-15"),
        (25000, "Salary", "2024-02-01"),
        (3000, "Bonus", "2024-02-28"),
        (25000, "Salary", "2024-03-01"),
        (4500, "Freelance", "2024-03-15"),
        (25000, "Salary", "2024-04-01"),
        (6000, "Investment", "2024-04-10"),
    ]

    # Clear existing data
    cursor.execute("DELETE FROM expenses")
    cursor.execute("DELETE FROM income")

    # Insert expenses
    for expense in expenses_data:
        cursor.execute(
            "INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?)",
            expense
        )

    # Insert income
    for income in income_data:
        cursor.execute(
            "INSERT INTO income (source, amount, date) VALUES (?, ?, ?)",
            income
        )

    conn.commit()
    conn.close()
    print("✅ Sample data generated successfully!")
    print(f"   - Added {len(expenses_data)} expenses")
    print(f"   - Added {len(income_data)} income entries")

if __name__ == "__main__":
    generate_sample_data()
