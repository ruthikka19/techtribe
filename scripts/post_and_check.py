import urllib.parse, urllib.request
import json
import sqlite3

BASE = 'http://127.0.0.1:5000'

def post(path, data):
    url = BASE + path
    data = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req) as r:
        return r.read().decode()

if __name__ == '__main__':
    print('Posting test expense...')
    post('/add_expense', {'amount':'77.77','category':'AutoTest','date':'2026-02-12','description':'post_and_check expense'})
    print('Posting test income...')
    post('/add_income', {'source':'AutoSalary','amount':'999.99','date':'2026-02-12'})
    print('Posting test budget...')
    # use current month
    from datetime import datetime
    m = datetime.now().strftime('%Y-%m')
    post('/set_budget', {'category':'AutoTest','limit':'5000','month':m})
    print('Posting test savings goal...')
    post('/savings_goals', {'goal_name':'AutoGoal','target_amount':'1500','deadline':'2026-12-31'})

    print('\nNow checking database (last 5 rows per table):')
    DB = 'database.db'
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    for tbl in ['expenses','income','budgets','savings_goals']:
        print(f'-- {tbl} --')
        try:
            c.execute(f'SELECT * FROM {tbl} ORDER BY id DESC LIMIT 5')
            for r in c.fetchall():
                print(dict(r))
        except Exception as e:
            print('error', e)
    conn.close()
