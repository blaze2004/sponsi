"""Middleware to manage redirection based on user authentication and role"""

from flask import redirect, request, url_for
from flask_login import current_user


def middleware():
    """Core Middleware"""

    if request.path.startswith("/static"):
        return None

    if (
        request.path != "/"
        and not current_user.is_authenticated
        and not request.path.startswith("/auth")
    ):
        return redirect(url_for("auth.signin"))

    if current_user.is_authenticated:
        if current_user.onboarded is False:
            if request.path != "/auth/onboarding":
                return redirect(url_for("auth.onboarding"))
            return None
        if request.path == "/":
            return redirect(url_for("main.dashboard"))

        if request.path.startswith("/auth") and request.path != "/auth/signout":
            return redirect(url_for("main.dashboard"))
    return None
