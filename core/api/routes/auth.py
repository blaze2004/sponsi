"""Auth routes."""

from hmac import compare_digest
from flask import Blueprint, redirect, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from utils import db
from api.forms.auth import (
    AdminOnboardingForm,
    InfluencerOnboardingForm,
    SignUpForm,
    SponsorOnboardingForm,
)
from api.models.user import PlatformPresence, User, UserRole

auth = Blueprint("auth", __name__)


@auth.route("/status", methods=["GET"])
def status():
    """Check if user is authenticated."""

    if current_user.is_authenticated:
        return {
            "isAuthenticated": True,
            "role": current_user.role.name,
            "onboarded": current_user.onboarded,
        }

    return {
        "isAuthenticated": False,
        "role": None,
        "onboarded": None,
    }


@auth.route("/signin", methods=["POST"])
def signin():
    """Authenticate the user."""

    if current_user.is_authenticated:
        return redirect("/dashboard")

    email = request.json.get("email")
    password = request.json.get("password")

    if not email or not password:
        return {"message": "Email and password are required."}, 400

    user = db.session.execute(db.select(User).where(User.email == email)).scalar()

    if user and user.check_password(password):
        login_user(user, remember=True)
        return {
            "isAuthenticated": True,
            "role": user.role.name,
            "onboarded": user.onboarded,
        }
    else:
        return {"message": "Invalid email or password."}, 400


@auth.route("/signup", methods=["POST"])
def signup():
    """Register new user."""

    form = SignUpForm(request.form)

    if form.validate():
        user_exists = db.session.execute(
            db.select(User).where(User.email == form.email.data)
        ).scalar()

        print(user_exists)

        if user_exists:
            return {"message": "User already exists."}, 400

        user = User(
            email=form.email.data,
            name=form.name.data,
            role=UserRole(form.role.data).name,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return {"message": "User created successfully."}, 200

    error_msg = form.errors.popitem()[1][-1]
    return {"message": error_msg}, 400


@auth.route("/signout", methods=["POST"])
@login_required
def signout():
    """Sign out the user."""
    logout_user()
    return redirect(url_for("main.index"))


@auth.route("/onboarding", methods=["POST"])
@login_required
def onboarding():
    """Handle User Onboarding according to role."""

    if current_user.onboarded is True:
        return redirect("/dashboard")

    if current_user.role == UserRole.SPONSOR:
        form = SponsorOnboardingForm(request.form)

        if form.validate():
            current_user.company_name = form.company_name.data
            current_user.industry = form.industry.data
            current_user.website = form.website.data
            current_user.about = form.about.data
            current_user.monthly_budget = form.monthly_budget.data
            current_user.onboarded = True
            db.session.commit()
            return {"message": "Onboarding completed successfully."}, 200
        error_msg = form.errors.popitem()[1][-1]

        return {"message": error_msg}, 400

    if current_user.role == UserRole.INFLUENCER:
        form = InfluencerOnboardingForm(request.form)

        if form.validate():
            current_user.niche = form.niche.data
            current_user.category = form.category.data
            current_user.website = form.website.data
            current_user.about = form.about.data

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
            return {"message": "Onboarding completed successfully."}, 200

        error = form.errors.popitem()
        if error[0] == "platforms":
            error_msg = error[1][0].popitem()[1][-1]
        else:
            error_msg = error[1][-1]

        return {"message": error_msg}, 400

    # Admin onboarding (Admin users need to reset their password on first login)
    form = AdminOnboardingForm(request.form)

    error_msg = None
    if form.validate():
        if current_user.check_password(form.password.data):
            error_msg = "Password cannot be the same as the previous one."
        else:
            current_user.set_password(form.password.data)
            current_user.onboarded = True
            db.session.commit()
            return {"message": "Onboarding completed successfully."}, 200
    error_msg = error_msg or form.errors.popitem()[1][-1]

    return {"message": error_msg}, 400
