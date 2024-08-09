"""Marketing Pages views."""

from flask import Blueprint, render_template

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Render the landing page."""
    return render_template("index.html")

@main.route("/dashboard")
def dashboard():
    """Render the dashboard according to user role."""
    return render_template("index.html")
