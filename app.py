from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def booking():
    return render_template("booking.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/tests")
def tests():
    return render_template("tests.html")


@app.route("/book-test")
def book_test():
    return render_template("book_test.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
