"""Admin actions Pages views."""

from flask import Blueprint, request
from flask_login import current_user, login_required

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
