from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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

@app.route("/messages")
def messages():

    all_messages = ContactMessage.query.all()

    return render_template(

        "messages.html",

        messages=all_messages
    )


with app.app_context():

    db.create_all()


if __name__ == "__main__":

    app.run(debug=True)