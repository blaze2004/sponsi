"""Auth Pages views."""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from src.app.forms.auth import (
    AdminOnboardingForm,
    InfluencerOnboardingForm,
    SignUpForm,
    SponsorOnboardingForm,
)
from src.app.utils import db
from src.app.models.user import PlatformPresence, User, UserRole

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

    form = SignUpForm(request.form)

    if request.method == "POST":
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

    return render_template("auth/signup.html", data=form.data)


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
        form = SponsorOnboardingForm(request.form)
        if request.method == "POST":
            if form.validate():
                current_user.company_name = form.company_name.data
                current_user.industry = form.industry.data
                current_user.website = form.website.data
                current_user.onboarded = True
                db.session.commit()
                flash("User updated successfully.", "success")
                return redirect(url_for("main.dashboard"))
            error_msg = form.errors.popitem()[1][-1]
            flash(error_msg, "danger")
        return render_template("auth/onboarding/sponsor.html", data=form.data)

    if current_user.role == UserRole.INFLUENCER:
        form = InfluencerOnboardingForm(request.form)

        if request.method == "POST":
            if form.validate():
                current_user.niche = form.niche.data
                current_user.audience_size = form.audience_size.data
                current_user.website = form.website.data

                for platform in form.platforms.data:
                    db.session.add(
                        PlatformPresence(
                            user_id=current_user.id,
                            platform=platform["platform"],
                            username=platform["username"],
                            url=platform["url"],
                            followers=platform["followers"],
                        )
                    )

                current_user.onboarded = True
                db.session.commit()
                flash("User updated successfully.", "success")
                return redirect(url_for("main.dashboard"))

            error = form.errors.popitem()
            if error[0] == "platforms":
                error_msg = error[1][0].popitem()[1][-1]
            else:
                error_msg = error[1][-1]
            flash(error_msg, "danger")
        return render_template("auth/onboarding/influencer.html", data=form.data)

    # Admin onboarding (Admin and SuperAdmin users need to reset their password on first login)
    form = AdminOnboardingForm(request.form)

    if request.method == "POST":
        error_msg = None
        if form.validate():
            if current_user.check_password(form.password.data):
                error_msg = "Password cannot be the same as the previous one."
            else:
                current_user.set_password(form.password.data)
                current_user.onboarded = True
                db.session.commit()
                flash("Password updated successfully.", "success")
                return redirect(url_for("main.dashboard"))
        error_msg = error_msg or form.errors.popitem()[1][-1]
        flash(error_msg, "danger")
    return render_template("auth/onboarding/admin.html", data=form.data)
