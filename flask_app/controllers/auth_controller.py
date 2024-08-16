from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from flask_app.models import get_db_connection
from flask_app.models.auth import User

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.before_request
def check_session():
    if "user_id" not in session and "role" in session:
        session.clear()


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("auth/apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session or session.get("role") != "administrator":
            flash("You do not have permission to access this page.", "error")
            return redirect(url_for("auth_bp.login"))
        return f(*args, **kwargs)

    return decorated_function


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    session.clear()

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        date_of_birth = request.form.get("date_of_birth")
        phone = request.form.get("phone")        
        street = request.form.get("street")
        city = request.form.get("city")
        state = request.form.get("state")
        zip_ = request.form.get("zip")
        photo = "https://i.pinimg.com/236x/c9/f7/d6/c9f7d650ce2a7f0f63ee7b1691694229.jpg"

        error, user_id = User.register(
            email, password, first_name, last_name, date_of_birth, phone, street, city, state, zip_, photo
        )

        if error:
            return apology(error, 400)

        # AuthClient.add_client(
        #     first_name, last_name, date_of_birth, email, phone, street, city, state, zip_, photo
        # )

        return redirect("/in")

    return render_template("auth/register.html", client_form=True, show_user_info=False)




@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return apology("Must provide email and password", 403)

        user = User.login(email, password)

        if not user:
            return apology("Invalid email and/or password", 403)

        return redirect("/in")
    else:
        return render_template("auth/login.html", show_user_info=False)


@auth_bp.route("/logout")
def logout():
    User.logout()
    return redirect("/")


@auth_bp.route("/edit_password", methods=["GET", "POST"])
@login_required
def edit_password():
    conn = get_db_connection()
    if request.method == "POST":
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password:
            flash("Must provide password", "error")
            return render_template("auth/edit_password.html")
        if not confirmation:
            flash("Must provide confirmation", "error")
            return render_template("auth/edit_password.html")
        if password != confirmation:
            flash("Passwords do not match", "error")
            return render_template("auth/edit_password.html")
        hashed_pass = generate_password_hash(password)
        conn.execute(
            "UPDATE Users SET password = ? WHERE id = ?",
            (hashed_pass, session["user_id"]),
        )
        conn.commit()
        conn.close()
        flash("Password updated successfully", "success")
        return redirect("/")
    conn.close()
    return render_template("auth/edit_password.html")
