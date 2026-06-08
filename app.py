from flask import Flask, render_template, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("coffee.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coffee (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            votes INTEGER DEFAULT 0
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM coffee")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            "INSERT INTO coffee (name, votes) VALUES (?, ?)",
            [
                ("Cappuccino", 0),
                ("Latte", 0),
                ("Espresso", 0),
                ("Mocha", 0),
                ("Cold Coffee", 0)
            ]
        )

    conn.commit()
    conn.close()

@app.route("/")
def home():
    conn = sqlite3.connect("coffee.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM coffee")
    coffees = cursor.fetchall()

    conn.close()

    return render_template("index.html", coffees=coffees)

@app.route("/vote/<int:coffee_id>")
def vote(coffee_id):
    conn = sqlite3.connect("coffee.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE coffee SET votes = votes + 1 WHERE id = ?",
        (coffee_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)