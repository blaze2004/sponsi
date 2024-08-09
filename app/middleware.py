"""Middleware to manage redirection based on user authentication and role"""

from flask import redirect, request, url_for
from flask_login import current_user


def middleware():
    """Core Middleware"""

    if request.path != "/" and not current_user.is_authenticated:
        return redirect(url_for("auth.signin"))

    if current_user.is_authenticated:
        if request.path == "/":
            return redirect(url_for("main.dashboard"))

        if request.path.startswith("/auth") and request.path != "/auth/signout":
            return redirect(url_for("main.dashboard"))
    return None
