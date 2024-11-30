"""Marketing Pages views."""

from flask import Blueprint, render_template
from flask_login import login_required

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Render the landing page."""
    return render_template("index.html")


@main.route("/dashboard")
@login_required
def dashboard():
    """Render the dashboard."""
    return {"message": "Welcome to the dashboard."}
