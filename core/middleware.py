"""Middleware to manage redirection based on user authentication and role"""

from flask import redirect, render_template, request, url_for
from flask_login import current_user


def middleware():
    """Core Middleware"""

    if request.path.startswith("/src/"):
        return redirect("http://localhost:5173" + request.path)  # vite dev server

    if request.path.startswith("/assets"):
        return redirect("/static" + request.path)

    if request.path.startswith("/static"):
        return None

    if request.path.startswith("/api"):
        if request.path == "/api/auth/status":
            return None

        if not current_user.is_authenticated and not request.path.startswith(
            "/api/auth"
        ):
            return redirect("/signin")

        if current_user.is_authenticated:
            if current_user.onboarded is False:
                if request.path != "/api/auth/onboarding":
                    return redirect("/onboarding")
                return None

            if request.path.startswith("/api/auth") and (
                request.path != "/api/auth/signout"
            ):
                return redirect("/dashboard")
        return None

    if request.path == "/":
        if current_user.is_authenticated:
            return redirect("/dashboard")
        return None

    if request.path in ("/signin", "/signup") and current_user.is_authenticated:
        return redirect("/dashboard")

    if request.path == "/onboarding":
        if current_user.is_authenticated and current_user.onboarded:
            return redirect("/dashboard")

    return render_template("index.html")
