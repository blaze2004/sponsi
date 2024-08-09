"""Auth Pages views."""

from flask import Blueprint, flash, render_template, request
from flask_login import current_user, login_user
from app.utils import db
from app.models.user import User

auth = Blueprint("auth", __name__)


@auth.route("/signin", methods=["GET", "POST"])
def signin():
    """Render the Sign In page."""

    if current_user.is_authenticated:
        return "You are already logged in."
    
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()

        if user:
            if user.check_password(password):
                login_user(user)
                return "Login success"
            flash("Invalid password.", "danger")
        else:
            flash("Invalid email.", "danger")
    return render_template("auth/signin.html")

@auth.route("/signup")
def signup():
    """Render the Sign Up page."""
    return render_template("auth/signup.html")
