"""Influencer views."""

from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.models.campaigns import AdRequest, AdRequestStatus
from app.models.user import UserRole
from app.utils import db

influencer = Blueprint("influencer", __name__)


@influencer.route("/find")
@login_required
def find():
    """Find ad requests to apply for."""
    if current_user.role != UserRole.INFLUENCER:
        return redirect(url_for("main.dashboard"))

    ad_requests = db.session.execute(
        db.select(AdRequest).where(AdRequest.status != AdRequestStatus.ACCEPTED)
    ).scalars()

    ad_requests_data = []

    for ad_request in ad_requests:

        if current_user.id in (ad_request.requested_by_id, ad_request.requested_to_id):
            continue

        ad_requests_data.append(
            {
                "id": ad_request.id,
                "title": ad_request.title,
                "description": ad_request.description,
                "requirements": ad_request.requirements,
                "payment_amount": ad_request.payment_amount,
                "campaign": {
                    "title": ad_request.campaign.title,
                    "niche": ad_request.campaign.niche,
                },
                "sponsor": {
                    "name": ad_request.campaign.user.name,
                },
            }
        )

    return render_template("influencer/find.html", ad_requests=ad_requests_data)


@influencer.route("/ad-request/<int:ad_request_id>/apply", methods=["POST"])
@login_required
def apply(ad_request_id):
    """Apply for an ad request."""

    if current_user.role != UserRole.INFLUENCER:
        return {"message": "You are not authorized to perform this action."}, 403

    ad_request = db.session.execute(
        db.select(AdRequest).where(AdRequest.id == ad_request_id)
    ).scalar()

    if ad_request.status != AdRequestStatus.ACCEPTED and ad_request.requested_by_id:
        return {"message": "Ad request is not available."}, 403

    ad_request.requested_by_id = current_user.id

    db.session.commit()

    return {"message": "Applied for ad request successfully."}, 200
