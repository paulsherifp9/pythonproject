from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "secret123"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///messages.db"

db = SQLAlchemy(app)


class ContactMessage(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    email = db.Column(db.String(100))

    message = db.Column(db.Text)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/projects")
def projects():

    return render_template("projects.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():

    success = False

    if request.method == "POST":

        name = request.form["name"]

        email = request.form["email"]

        message = request.form["message"]

        new_message = ContactMessage(

            name=name,

            email=email,

            message=message
        )

        db.session.add(new_message)

        db.session.commit()

        success = True

    return render_template(

        "contact.html",

        success=success
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":

            session["user"] = username

            return redirect("/messages")

    return render_template("login.html")

@app.route("/messages")
def messages():

    if "user" not in session:

         return redirect("/login")

    all_messages = ContactMessage.query.all()

    return render_template(

        "messages.html",

        messages=all_messages
    )

@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login")


with app.app_context():

    db.create_all()


if __name__ == "__main__":

    app.run(debug=True)