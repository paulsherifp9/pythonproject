from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
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


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), unique=True)

    password = db.Column(db.String(100))

    role = db.Column(db.String(20), default="user")


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

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:

            flash("Username already exists")

            return redirect("/register")

        if username == "admin":

            user_role = "admin"

        else:

            user_role = "user"


        new_user = User(

    username=username,

    password=hashed_password,

    role=user_role
)

        db.session.add(new_user)

        db.session.commit()

        flash("Registration successful")

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        user = User.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            session["user"] = username

            if user.role == "admin":

                return redirect("/messages")

            else:

                return redirect("/")

        else:

            flash("Invalid username or password")

    return render_template("login.html")


@app.route("/messages")
def messages():

    if not session.get("user"):

        flash("Please login first")

        return redirect("/login")

    user = User.query.filter_by(
        username=session["user"]
    ).first()

    if not user or user.role != "admin":

        flash("Access denied")

        return redirect("/")

    search = request.args.get("search")

    if search:

        all_messages = ContactMessage.query.filter(

            ContactMessage.name.contains(search) |

            ContactMessage.email.contains(search) |

            ContactMessage.message.contains(search)

        ).all()

    else:

        all_messages = ContactMessage.query.all()

    return render_template(
        "messages.html",
        messages=all_messages
    )


@app.route("/dashboard")
def dashboard():

    if not session.get("user"):

        return redirect("/login")

    user = User.query.filter_by(
        username=session["user"]
    ).first()

    if not user or user.role != "admin":

        flash("Access denied")

        return redirect("/")

    total_users = User.query.count()

    total_messages = ContactMessage.query.count()

    total_admins = User.query.filter_by(
        role="admin"
    ).count()

    return render_template(

        "dashboard.html",

        total_users=total_users,

        total_messages=total_messages,

        total_admins=total_admins
    )

@app.route("/edit_user/<int:id>",
           methods=["GET", "POST"])
def edit_user(id):

    if not session.get("user"):

        return redirect("/login")

    admin = User.query.filter_by(
        username=session["user"]
    ).first()

    if not admin or admin.role != "admin":

        flash("Access denied")

        return redirect("/")

    user = User.query.get(id)

    if request.method == "POST":

        user.username = request.form["username"]

        user.role = request.form["role"]

        db.session.commit()

        flash("User updated successfully")

        return redirect("/users")

    return render_template(
        "edit_user.html",
        user=user
    )

@app.route("/delete_user/<int:id>")
def delete_user(id):

    if not session.get("user"):

        return redirect("/login")

    admin = User.query.filter_by(
        username=session["user"]
    ).first()

    if not admin or admin.role != "admin":

        flash("Access denied")

        return redirect("/")

    user = User.query.get(id)

    db.session.delete(user)

    db.session.commit()

    flash("User deleted successfully")

    return redirect("/users")

@app.route("/users")
def users():

    if not session.get("user"):

        return redirect("/login")

    user = User.query.filter_by(
        username=session["user"]
    ).first()

    if not user or user.role != "admin":

        flash("Access denied")

        return redirect("/")

    all_users = User.query.all()

    return render_template(
        "users.html",
        users=all_users
    )

@app.route("/edit_message/<int:id>",
           methods=["GET", "POST"])
def edit_message(id):

    if not session.get("user"):

        return redirect("/login")

    user = User.query.filter_by(
        username=session["user"]
    ).first()

    if not user or user.role != "admin":

        flash("Access denied")

        return redirect("/")

    message = ContactMessage.query.get(id)

    if request.method == "POST":

        message.name = request.form["name"]

        message.email = request.form["email"]

        message.message = request.form["message"]

        db.session.commit()

        flash("Message updated successfully")

        return redirect("/messages")

    return render_template(
        "edit_message.html",
        message=message
    )

@app.route("/delete_message/<int:id>")
def delete_message(id):

    if not session.get("user"):

        return redirect("/login")

    user = User.query.filter_by(
        username=session["user"]
    ).first()

    if not user or user.role != "admin":

        flash("Access denied")

        return redirect("/")

    message = ContactMessage.query.get(id)

    db.session.delete(message)

    db.session.commit()

    flash("Message deleted successfully")

    return redirect("/messages")



@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login")


with app.app_context():

    db.create_all()


if __name__ == "__main__":

    app.run(debug=True)