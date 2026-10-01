from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import date

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

DATABASE = "bookings.db"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"


def init_db():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mobile TEXT NOT NULL,
            test TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def booking():

    if request.method == "POST":

        name = request.form["name"]
        mobile = request.form["mobile"]
        test = request.form["test"]
        booking_date = request.form["date"]

        conn = sqlite3.connect(DATABASE)

        conn.execute(
            "INSERT INTO bookings (name, mobile, test, date) VALUES (?, ?, ?, ?)",
            (name, mobile, test, booking_date)
        )

        conn.commit()
        conn.close()

        return "Booking successfully received! ✅"

    return render_template("booking.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/admin")

        return "Wrong username or password ❌"

    return render_template("login.html")


@app.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect("/login")

    search = request.args.get("search", "")

    conn = sqlite3.connect(DATABASE)

    if search:

        bookings = conn.execute(
            """
            SELECT * FROM bookings
            WHERE name LIKE ? OR mobile LIKE ?
            ORDER BY id DESC
            """,
            (f"%{search}%", f"%{search}%")
        ).fetchall()

    else:

        bookings = conn.execute(
            "SELECT * FROM bookings ORDER BY id DESC"
        ).fetchall()

    total_bookings = conn.execute(
        "SELECT COUNT(*) FROM bookings"
    ).fetchone()[0]

    today = date.today().isoformat()

    today_bookings = conn.execute(
        "SELECT COUNT(*) FROM bookings WHERE date = ?",
        (today,)
    ).fetchone()[0]

    conn.close()

    return render_template(
        "admin.html",
        bookings=bookings,
        total_bookings=total_bookings,
        today_bookings=today_bookings,
        search=search
    )
@app.route("/edit/<int:booking_id>", methods=["GET", "POST"])
def edit_booking(booking_id):

    conn = sqlite3.connect(DATABASE)

    if request.method == "POST":

        name = request.form["name"]
        mobile = request.form["mobile"]
        test = request.form["test"]
        booking_date = request.form["date"]

        conn.execute(
            """
            UPDATE bookings
            SET name = ?, mobile = ?, test = ?, date = ?
            WHERE id = ?
            """,
            (name, mobile, test, booking_date, booking_id)
        )

        conn.commit()
        conn.close()

        return redirect("/admin")

    booking = conn.execute(
        "SELECT * FROM bookings WHERE id = ?",
        (booking_id,)
    ).fetchone()

    conn.close()

    return render_template("edit.html", booking=booking)
@app.route("/delete/<int:booking_id>", methods=["POST"])
def delete_booking(booking_id):

    if not session.get("admin"):
        return redirect("/login")

    conn = sqlite3.connect(DATABASE)

    conn.execute(
        "DELETE FROM bookings WHERE id = ?",
        (booking_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/admin")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


init_db()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
