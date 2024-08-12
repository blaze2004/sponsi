"""Admin actions Pages views."""

from flask import Blueprint, request
from flask_login import current_user, login_required

from app.models.campaigns import Campaign
from app.models.user import User, UserRole
from app.utils import db

admin = Blueprint("admin", __name__)


@admin.route("/flag/user", methods=["POST"])
@login_required
def flag_user():
    """Flag user handler."""

    if current_user.role not in (UserRole.ADMIN, UserRole.SUPERADMIN):
        return {"message": "You are not allowed to perform this action."}, 403

    user_id = request.json.get("user_id")
    reason = request.json.get("flagged_reason")

    if not user_id:
        return {"message": "UserId is required."}, 400

    if not reason:
        return {"message": "A valid reason is required."}, 400

    user = db.session.execute(db.select(User).where(User.id == user_id)).scalar()

    if not user:
        return {"message": "User not found."}, 404

    if user.flagged:
        return {"message": "User already flagged."}, 400

    user.flagged = True
    user.flagged_reason = reason
    db.session.commit()

    return {"message": "User flagged successfully."}, 200


@admin.route("/unflag/user", methods=["POST"])
@login_required
def unflag_user():
    """Unflag user handler."""

    if current_user.role not in (UserRole.ADMIN, UserRole.SUPERADMIN):
        return {"message": "You are not allowed to perform this action."}, 403

    user_id = request.json.get("user_id")

    if not user_id:
        return {"message": "UserId is required."}, 400

    user = db.session.execute(db.select(User).where(User.id == user_id)).scalar()

    if not user:
        return {"message": "User not found."}, 404

    if not user.flagged:
        return {"message": "User is not flagged."}, 400

    user.flagged = False
    user.flagged_reason = None
    db.session.commit()

    return {"message": "User unflagged successfully."}, 200


@admin.route("/flag/campaign", methods=["POST"])
@login_required
def flag_campaign():
    """Flag campaign handler."""

    if current_user.role not in (UserRole.ADMIN, UserRole.SUPERADMIN):
        return {"message": "You are not allowed to perform this action."}, 403

    campaign_id = request.json.get("campaign_id")
    reason = request.json.get("flagged_reason")

    if not campaign_id:
        return {"message": "Campaign Id is required."}, 400

    if not reason:
        return {"message": "A valid reason is required."}, 400

    campaign = db.session.execute(
        db.select(Campaign).where(Campaign.id == campaign_id)
    ).scalar()

    if not campaign:
        return {"message": "Campaign not found."}, 404

    if campaign.flagged:
        return {"message": "Campaign already flagged."}, 400

    campaign.flagged = True
    campaign.flagged_reason = reason
    db.session.commit()

    return {"message": "Campaign flagged successfully."}, 200


@admin.route("/unflag/campaign", methods=["POST"])
@login_required
def unflag_campaign():
    """Unflag campaign handler."""

    if current_user.role not in (UserRole.ADMIN, UserRole.SUPERADMIN):
        return {"message": "You are not allowed to perform this action."}, 403

    campaign_id = request.json.get("campaign_id")

    if not campaign_id:
        return {"message": "Campaign Id is required."}, 400

    campaign = db.session.execute(
        db.select(Campaign).where(Campaign.id == campaign_id)
    ).scalar()

    if not campaign:
        return {"message": "Campaign not found."}, 404

    if not campaign.flagged:
        return {"message": "Campaign is not flagged."}, 400

    campaign.flagged = False
    campaign.flagged_reason = None
    db.session.commit()

    return {"message": "Campaign unflagged successfully."}, 200


@admin.route("/create-admin", methods=["POST"])
@login_required
def create_admin():
    """Create admin handler."""

    if current_user.role != UserRole.SUPERADMIN:
        return {"message": "You are not allowed to perform this action."}, 403

    email = request.json.get("email")
    name = request.json.get("name")
    password = request.json.get("password")

    if not name:
        return {"message": "Name is required."}, 400

    if not email:
        return {"message": "Email is required."}, 400

    if not password:
        return {"message": "Password is required."}, 400

    if db.session.execute(db.select(User).where(User.email == email)).scalar():
        return {"message": "User already exists."}, 400

    user = User(email=email, role=UserRole.ADMIN, name=name)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return {"message": "Admin created successfully."}, 200
