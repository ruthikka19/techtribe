# Expense Tracker (local)

This project runs a small Flask app to track income, expenses, budgets and savings goals.

Quick start (Windows, using provided venv):

1. Activate the virtualenv (if you use the included `.venv`):

```powershell
C:/Users/MaanuRuthi/OneDrive/Desktop/techtribe/.venv/Scripts/Activate.ps1
```

2. Install dependencies (if needed):

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
C:/Users/MaanuRuthi/OneDrive/Desktop/techtribe/.venv/Scripts/python.exe app.py
```

4. Open in your browser:

- Home: http://127.0.0.1:5000/home
- Dashboard: http://127.0.0.1:5000/

Editing templates:

- Templates are in the `templates/` folder. With the server running in debug mode, changes to templates should auto-reload.
- If you make changes and they don't appear, stop the server and restart.

Theme toggle:

- A floating theme button (top-right) toggles light/dark and persists to `localStorage`.

If you want, I can package the site or create a single-file demo you can run elsewhere.