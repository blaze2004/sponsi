"""Auth Pages views."""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app.forms.auth import SignUpForm
from app.utils import db
from app.models.user import User, UserRole

auth = Blueprint("auth", __name__)


@auth.route("/signin", methods=["GET", "POST"])
def signin():
    """Render the Sign In page."""

    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Email and password are required.", "danger")
        else:
            user = db.session.execute(
                db.select(User).where(User.email == email)
            ).scalar()

            if user:
                if user.check_password(password):
                    login_user(user, remember=True)
                    return redirect(url_for("main.dashboard"))
                flash("Invalid password.", "danger")
            else:
                flash("Invalid email.", "danger")
    return render_template("auth/signin.html")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    """Render the Sign Up page."""

    if request.method == "POST":
        form = SignUpForm(request.form)
        if form.validate():
            user_exists = db.session.execute(
                db.select(User).where(User.email == form.email.data)
            ).scalar()

            print(user_exists)

            if user_exists:
                flash("User already exists.", "danger")
            else:
                user = User(
                    email=form.email.data,
                    name=form.name.data,
                    role=UserRole(form.role.data).name,
                )
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                flash("User created successfully.", "success")
                return redirect(url_for("auth.signin"))
        else:
            error_msg = form.errors.popitem()[1][-1]
            flash(error_msg, "danger")

    return render_template("auth/signup.html")


@auth.route("/signout", methods=["POST"])
def signout():
    """Sign out the user."""
    logout_user()
    return redirect(url_for("main.index"))


@auth.route("/onboarding", methods=["GET", "POST"])
@login_required
def onboarding():
    """Render the Onboarding page according to user role."""

    if current_user.onboarded is True:
        return redirect(url_for("main.dashboard"))

    if current_user.role == UserRole.SPONSOR:
        return render_template("auth/onboarding/sponsor.html")
    return render_template("auth/onboarding.html")
