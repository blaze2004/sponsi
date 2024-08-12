"""Sponsor views."""

from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.forms.campaign import CreateOrUpdateAdRequestsForm, CreateOrUpdateCampaignForm
from app.models.campaigns import AdRequest, Campaign, CampaignVisibility, Message
from app.models.user import User, UserRole
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


@sponsor.route("/campaigns/<int:campaign_id>/ads", methods=["GET", "POST"])
@login_required
def campaign_ad_requests(campaign_id):
    """Get all ads for a campaign."""

    if current_user.role != UserRole.SPONSOR:
        return redirect(url_for("main.dashboard"))

    campaign = db.session.execute(
        db.select(Campaign).where(Campaign.id == campaign_id)
    ).scalar()

    if not campaign:
        flash("Campaign not found.", "danger")
        return redirect(url_for("sponsor.campaigns"))

    if campaign.sponsor_id != current_user.id:
        flash("You are not allowed to perform this action.", "danger")
        return redirect(url_for("sponsor.campaigns"))

    form = CreateOrUpdateAdRequestsForm(request.form)
    show_form_modal = False

    if request.method == "POST":
        if form.validate():
            ad_request = AdRequest(
                campaign_id=campaign_id,
                title=form.title.data,
                description=form.description.data,
                payment_amount=form.payment_amount.data,
                requirements=form.requirements.data,
            )

            db.session.add(ad_request)
            db.session.commit()
            flash("Ad request created successfully.", "success")
            return redirect(
                url_for("sponsor.campaign_ad_requests", campaign_id=campaign_id)
            )

        error_msg = form.errors.popitem()[1][-1]
        flash(error_msg, "danger")
        show_form_modal = True

    ad_requests = db.session.execute(
        db.select(AdRequest).where(AdRequest.campaign_id == campaign_id)
    ).scalars()

    ad_requests_data = []

    for ad_request in ad_requests:
        ad_requests_data.append(
            {
                "id": ad_request.id,
                "campaign_id": ad_request.campaign_id,
                "influencer_id": ad_request.influencer_id,
                "status": ad_request.status.name,
                "title": ad_request.title,
                "description": ad_request.description,
                "payment_amount": ad_request.payment_amount,
                "requirements": ad_request.requirements,
            }
        )

    return render_template(
        "sponsor/ad_request.html",
        data=form.data,
        campaign=campaign,
        ad_requests=ad_requests_data,
        show_form_modal=show_form_modal,
    )


@sponsor.route(
    "/campaigns/<int:campaign_id>/ads/<int:ad_request_id>", methods=["PUT", "DELETE"]
)
@login_required
def edit_or_delete_ad_request(campaign_id, ad_request_id):
    """Edit/Delete ad request handler."""

    if current_user.role != UserRole.SPONSOR:
        return {"message": "You are not allowed to perform this action."}, 403

    if request.method == "DELETE":
        ad_request = db.session.execute(
            db.select(AdRequest).where(AdRequest.id == ad_request_id)
        ).scalar()

        if not ad_request:
            return {"message": "Ad request not found."}, 404

        if ad_request.campaign.sponsor_id != current_user.id:
            return {"message": "You are not allowed to perform this action."}, 403

        db.session.delete(ad_request)
        db.session.commit()

        return {"message": "Ad request deleted successfully."}, 200

    form = CreateOrUpdateAdRequestsForm()

    for key, value in request.json.items():
        form[key].data = value if key != "payment_amount" else float(value)

    if form.validate():
        ad_request = db.session.execute(
            db.select(AdRequest).where(AdRequest.id == ad_request_id)
        ).scalar()

        if not ad_request:
            return {"message": "Ad request not found."}, 404

        if ad_request.campaign.sponsor_id != current_user.id:
            return {"message": "You are not allowed to perform this action."}, 403

        ad_request.title = form.title.data
        ad_request.description = form.description.data
        ad_request.payment_amount = form.payment_amount.data
        ad_request.requirements = form.requirements.data

        db.session.commit()

        return {"message": "Ad request updated successfully."}, 200

    error_msg = form.errors.popitem()[1][-1]
    return {"message": error_msg}, 400


@sponsor.route("/influencers")
@login_required
def influencers():
    """Get all influencers."""

    if current_user.role != UserRole.SPONSOR:
        return redirect(url_for("main.dashboard"))

    ad_requests = db.session.execute(
        db.select(AdRequest)
        .join(AdRequest.campaign)
        .where(
            (Campaign.sponsor_id == current_user.id), (AdRequest.influencer_id == None)
        )
    ).scalars()

    ad_requests_data = []

    for ad_request in ad_requests:
        ad_requests_data.append(
            {
                "id": ad_request.id,
                "campaign_id": ad_request.campaign_id,
                "influencer_id": ad_request.influencer_id,
                "title": ad_request.title,
                "campaign_title": ad_request.campaign.title,
            }
        )

    _influencers = db.session.execute(
        db.select(User).where(
            (User.role == UserRole.INFLUENCER), (User.flagged == False)
        )
    ).scalars()

    influencers_data = []

    for influencer in _influencers:
        influencers_data.append(
            {
                "id": influencer.id,
                "name": influencer.name,
                "about": influencer.about,
                "website": influencer.website,
                "niche": influencer.niche,
                "audience_size": influencer.audience_size,
                "platforms": [
                    {
                        "platform": platform.platform,
                        "username": platform.username,
                        "url": platform.url,
                        "followers": platform.followers,
                    }
                    for platform in influencer.platforms
                ],
            }
        )

    return render_template(
        "sponsor/find.html", influencers=influencers_data, ad_requests=ad_requests_data
    )


@sponsor.route("/influencers/<int:influencer_id>/ad-request", methods=["POST"])
@login_required
def invite_influencer_to_ad_request(influencer_id):
    """Invite influencer to ad request handler."""

    if current_user.role != UserRole.SPONSOR:
        return {"message": "You are not allowed to perform this action."}, 403

    influencer = db.session.execute(
        db.select(User).where(
            (User.id == influencer_id), (User.role == UserRole.INFLUENCER)
        )
    ).scalar()

    if not influencer:
        return {"message": "Influencer not found."}, 404

    if influencer.flagged:
        return {"message": "Influencer is flagged."}, 400

    ad_request_id = request.json.get("ad_request_id")

    ad_request = db.session.execute(
        db.select(AdRequest).where(AdRequest.id == ad_request_id)
    ).scalar()

    if not ad_request:
        return {"message": "Ad request not found."}, 404

    if ad_request.campaign.sponsor_id != current_user.id:
        return {"message": "You are not allowed to perform this action."}, 403

    ad_request.requested_to_id = influencer_id
    db.session.commit()

    return {"message": "Successfully sent ad request invite."}, 200


@sponsor.route(
    "/campaigns/<int:campaign_id>/ad_request/<int:ad_request_id>/chat",
    methods=["GET", "POST"],
)
@login_required
def chat(campaign_id, ad_request_id):
    """Chat with influencer handler."""

    if current_user.role not in (UserRole.SPONSOR, UserRole.INFLUENCER):
        return redirect(url_for("main.dashboard"))

    ad_request = db.session.execute(
        db.select(AdRequest).where(AdRequest.id == ad_request_id)
    ).scalar()

    if not ad_request:
        flash("Ad request not found.", "danger")
        return redirect(
            url_for("sponsor.campaign_ad_requests", campaign_id=campaign_id)
        )

    messages = []
    receivers = {}

    if request.method == "POST":
        message = request.form.get("message")
        receiver_id = request.form.get("receiver_id")

        if message and receiver_id:

            new_message = Message(
                message=message,
                receiver_id=receiver_id,
                sender_id=current_user.id,
                ad_request_id=ad_request_id,
            )

            db.session.add(new_message)
            db.session.commit()
            flash("Message sent successfully.", "success")
        else:
            flash("Message cannot be empty.", "danger")

    for msg in ad_request.messages:
        if current_user.role == UserRole.SPONSOR:
            if msg.sender_id != current_user.id and msg.sender_id not in receivers:
                receivers[msg.sender_id] = msg.sender.name

            if msg.receiver_id != current_user.id and msg.receiver_id not in receivers:
                receivers[msg.receiver_id] = msg.receiver.name

            messages.append(
                {
                    "id": msg.id,
                    "message": msg.message,
                    "receiver_id": msg.receiver_id,
                    "sender_id": msg.sender_id,
                    "sender_name": msg.sender.name,
                    "receiver_name": msg.receiver.name,
                }
            )
        elif current_user.role == UserRole.INFLUENCER:
            if msg.receiver_id == current_user.id or msg.sender_id == current_user.id:
                if msg.sender_id != current_user.id and msg.sender_id not in receivers:
                    receivers[msg.sender_id] = msg.sender.name

                if (
                    msg.receiver_id != current_user.id
                    and msg.receiver_id not in receivers
                ):
                    receivers[msg.receiver_id] = msg.receiver.name
                messages.append(
                    {
                        "id": msg.id,
                        "message": msg.message,
                        "receiver_id": msg.receiver_id,
                        "sender_id": msg.sender_id,
                        "sender_name": msg.sender.name,
                        "receiver_name": msg.receiver.name,
                    }
                )

    if ad_request.requested_to_id and ad_request.requested_to_id != current_user.id:
        if ad_request.requested_to_id not in receivers:
            receivers[ad_request.requested_to_id] = ad_request.requested_to.name

    if ad_request.requested_by_id and ad_request.requested_by_id != current_user.id:
        if ad_request.requested_by_id not in receivers:
            receivers[ad_request.requested_by_id] = ad_request.requested_by.name

    if ad_request.influencer_id and ad_request.infleuncer_id != current_user.id:
        if ad_request.influencer_id not in receivers:
            receivers[ad_request.influencer_id] = ad_request.influencer.name

    receivers = [{"id": k, "name": v} for k, v in receivers.items()]

    return render_template(
        "sponsor/chat.html",
        messages=messages,
        receivers=receivers,
        campaign_name=ad_request.campaign.title,
        ad_request_name=ad_request.title,
    )
