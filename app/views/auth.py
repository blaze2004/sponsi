"""Auth Pages views."""

from flask import Blueprint, render_template

auth = Blueprint("auth", __name__)


@auth.route("/signin")
def signin():
    """Render the Sign In page."""
    return render_template("auth/signin.html")


@auth.route("/signup")
def signup():
    """Render the Sign Up page."""
    return render_template("auth/signup.html")
