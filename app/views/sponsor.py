"""Sponsor views."""

from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.forms.campaign import CreateOrUpdateCampaignForm
from app.models.campaigns import Campaign, CampaignVisibility
from app.models.user import UserRole
from app.utils import db

sponsor = Blueprint("sponsor", __name__)


@sponsor.route("/campaigns", methods=["GET", "POST"])
@login_required
def campaigns():
    """Get all campaigns handler."""

    if current_user.role != UserRole.SPONSOR:
        return redirect(url_for("main.dashboard"))

    form = CreateOrUpdateCampaignForm(request.form)
    show_form_modal = False

    if request.method == "POST":
        if form.validate():

            campaign = Campaign(
                title=form.title.data,
                description=form.description.data,
                budget=form.budget.data,
                start_date=form.start_date.data,
                end_date=form.end_date.data,
                visibility=CampaignVisibility(form.visibility.data).name,
                niche=form.niche.data,
                goals=form.goals.data,
                sponsor_id=current_user.id,
            )

            db.session.add(campaign)
            db.session.commit()
            flash("Campaign created successfully.", "success")
            return redirect(url_for("sponsor.campaigns"))

        error_msg = form.errors.popitem()[1][-1]
        flash(error_msg, "danger")
        show_form_modal = True

    _campaigns = db.session.execute(
        db.select(Campaign).where(Campaign.sponsor_id == current_user.id)
    ).scalars()

    campaigns_data = []

    for campaign in _campaigns:
        if campaign.end_date < datetime.now():
            continue
        campaigns_data.append(
            {
                "id": campaign.id,
                "title": campaign.title,
                "description": campaign.description,
                "start_date": datetime.strftime(campaign.start_date, "%Y-%m-%d"),
                "end_date": datetime.strftime(campaign.end_date, "%Y-%m-%d"),
                "budget": campaign.budget,
                "visibility": campaign.visibility.name,
                "niche": campaign.niche,
                "goals": campaign.goals,
                "created_at": campaign.created_at,
                "flagged": campaign.flagged,
                "flagged_reason": campaign.flagged_reason,
            }
        )

    return render_template(
        "sponsor/campaigns.html",
        data=form.data,
        show_form_modal=show_form_modal,
        campaigns=campaigns_data,
    )


@sponsor.route("/campaigns/<int:campaign_id>", methods=["PUT", "DELETE"])
@login_required
def edit_or_delete_campaign(campaign_id):
    """Edit/Delete campaign handler."""

    if current_user.role != UserRole.SPONSOR:
        return {"message": "You are not allowed to perform this action."}, 403

    if request.method == "DELETE":
        campaign = db.session.execute(
            db.select(Campaign).where(Campaign.id == campaign_id)
        ).scalar()

        if not campaign:
            return {"message": "Campaign not found."}, 404

        if campaign.sponsor_id != current_user.id:
            return {"message": "You are not allowed to perform this action."}, 403

        db.session.delete(campaign)
        db.session.commit()

        return {"message": "Campaign deleted successfully."}, 200

    form = CreateOrUpdateCampaignForm()

    for key, value in request.json.items():
        if key in ("start_date", "end_date"):
            form[key].data = datetime.strptime(value, "%Y-%m-%d").date()
        else:
            form[key].data = value if key != "budget" else float(value)

    print(form.data)
    if form.validate():
        campaign = db.session.execute(
            db.select(Campaign).where(Campaign.id == campaign_id)
        ).scalar()

        if not campaign:
            return {"message": "Campaign not found."}, 404

        if campaign.sponsor_id != current_user.id:
            return {"message": "You are not allowed to perform this action."}, 403

        campaign.title = form.title.data
        campaign.description = form.description.data
        campaign.budget = form.budget.data
        campaign.start_date = form.start_date.data
        campaign.end_date = form.end_date.data
        campaign.visibility = CampaignVisibility(form.visibility.data).name
        campaign.niche = form.niche.data
        campaign.goals = form.goals.data

        db.session.commit()

        return {"message": "Campaign updated successfully."}, 200

    error_msg = form.errors.popitem()[1][-1]
    return {"message": error_msg}, 400
