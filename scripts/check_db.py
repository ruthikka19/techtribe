import sqlite3
from pprint import pprint

DB = 'database.db'
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
c = conn.cursor()

print('Last 3 expenses:')
c.execute('SELECT * FROM expenses ORDER BY id DESC LIMIT 3')
for r in c.fetchall():
    pprint(dict(r))

print('\nLast 3 incomes:')
c.execute('SELECT * FROM income ORDER BY id DESC LIMIT 3')
for r in c.fetchall():
    pprint(dict(r))

print('\nLast 3 budgets:')
c.execute('SELECT * FROM budgets ORDER BY id DESC LIMIT 3')
for r in c.fetchall():
    pprint(dict(r))

print('\nLast 3 savings_goals:')
c.execute('SELECT * FROM savings_goals ORDER BY id DESC LIMIT 3')
for r in c.fetchall():
    pprint(dict(r))

conn.close()
