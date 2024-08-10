"""Marketing Pages views."""

from flask import Blueprint, render_template
from flask_login import current_user, login_required
from app.models.user import User, UserRole
from app.utils import db

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Render the landing page."""
    return render_template("index.html")


@main.route("/dashboard")
@login_required
def dashboard():
    """Render the dashboard according to user role."""
    if current_user.role in (UserRole.ADMIN, UserRole.SUPERADMIN):
        users = db.session.execute(db.select(User).order_by(User.id)).scalars()
        users_data = []

        for user in users:
            users_data.append(
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role.name,
                    "about": user.about,
                    "flagged": user.flagged,
                    "flagged_reason": user.flagged_reason,
                    "onboarded": user.onboarded,
                    "website": user.website,
                    "company_name": user.company_name,
                    "industry": user.industry,
                    "platforms": [
                        {
                            "platform": platform.platform,
                            "username": platform.username,
                            "url": platform.url,
                            "followers": platform.followers,
                        }
                        for platform in user.platforms
                    ],
                    "niche": user.niche,
                    "audience_size": user.audience_size,
                }
            )
        return render_template("dashboard/admin.html", users=users_data)

    if current_user.role == UserRole.SPONSOR:
        return render_template("dashboard/sponsor.html")
    return render_template("dashboard.html")
