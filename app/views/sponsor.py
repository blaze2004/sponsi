"""Sponsor views."""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.forms.campaign import CreateCampaignForm
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

    form = CreateCampaignForm(request.form)
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

    return render_template(
        "sponsor/campaigns.html", data=form.data, show_form_modal=show_form_modal
    )
