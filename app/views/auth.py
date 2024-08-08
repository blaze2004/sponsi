"""Auth Pages views."""

from flask import Blueprint, render_template

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    """Render the login page."""
    return render_template("auth/login.html")


@auth.route("/register")
def register():
    """Render the register page."""
    return render_template("auth/register.html")
