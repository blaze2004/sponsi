"""Marketing Pages views."""

from datetime import datetime
from flask import Blueprint, render_template
from flask_login import current_user, login_required
from src.app.models.campaigns import (
    AdRequest,
    AdRequestStatus,
    Campaign,
    CampaignVisibility,
)
from src.app.models.user import User, UserRole
from src.app.utils import db

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

        campaigns = db.session.execute(
            db.select(Campaign).order_by(Campaign.id)
        ).scalars()
        campaigns_data = []

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

        for request in campaigns:
            campaigns_data.append(
                {
                    "id": request.id,
                    "title": request.title,
                    "description": request.description,
                    "start_date": datetime.strftime(request.start_date, "%Y-%m-%d"),
                    "end_date": datetime.strftime(request.end_date, "%Y-%m-%d"),
                    "budget": request.budget,
                    "visibility": request.visibility.name,
                    "niche": request.niche,
                    "goals": request.goals,
                    "created_at": request.created_at,
                    "flagged": request.flagged,
                    "flagged_reason": request.flagged_reason,
                    "sponsor": {
                        "id": request.user.id,
                        "name": request.user.name,
                        "email": request.user.email,
                        "role": request.user.role.name,
                        "about": request.user.about,
                        "flagged": request.user.flagged,
                        "flagged_reason": request.user.flagged_reason,
                        "onboarded": request.user.onboarded,
                        "website": request.user.website,
                        "company_name": request.user.company_name,
                        "industry": request.user.industry,
                    },
                }
            )

        ad_requests = db.session.execute(
            db.select(AdRequest).order_by(AdRequest.id)
        ).scalars()

        ad_requests_data = []

        for ad_request in ad_requests:
            ad_requests_data.append(
                {
                    "id": ad_request.id,
                    "title": ad_request.title,
                    "description": ad_request.description,
                    "campaign_id": ad_request.campaign_id,
                    "campaign": ad_request.campaign.title,
                    "influencer_id": ad_request.influencer_id,
                    "influencer": (
                        ad_request.influencer.name if ad_request.influencer else "N/A"
                    ),
                    "payment_amount": ad_request.payment_amount,
                    "status": ad_request.status.name,
                }
            )

        return render_template(
            "dashboard/admin.html",
            users=users_data,
            campaigns=campaigns_data,
            ad_requests=ad_requests_data,
        )

    if current_user.role == UserRole.SPONSOR:
        campaigns = db.session.execute(
            db.select(Campaign).where(Campaign.sponsor_id == current_user.id)
        ).scalars()

        campaigns_data = []

        for request in campaigns:
            if request.end_date < datetime.now():
                continue
            campaigns_data.append(
                {
                    "id": request.id,
                    "title": request.title,
                    "description": request.description,
                    "start_date": datetime.strftime(request.start_date, "%Y-%m-%d"),
                    "end_date": datetime.strftime(request.end_date, "%Y-%m-%d"),
                    "budget": request.budget,
                    "visibility": request.visibility.name,
                    "niche": request.niche,
                    "goals": request.goals,
                    "created_at": request.created_at,
                    "flagged": request.flagged,
                    "flagged_reason": request.flagged_reason,
                }
            )

        new_ad_requests = db.session.execute(
            db.select(AdRequest)
            .join(Campaign)
            .where(
                (Campaign.sponsor_id == current_user.id),
                (AdRequest.influencer_id == None),
            )
        ).scalars()

        new_ad_requests_data = []

        for ad_request in new_ad_requests:
            if (
                ad_request.requested_by_id is None
                and ad_request.requested_to_id is None
            ):
                continue

            new_ad_requests_data.append(
                {
                    "id": ad_request.id,
                    "title": ad_request.title,
                    "description": ad_request.description,
                    "campaign_id": ad_request.campaign_id,
                    "campaign": ad_request.campaign.title,
                    "influencer_id": (
                        ad_request.requested_by_id
                        if ad_request.requested_by_id
                        else ad_request.requested_to_id
                    ),
                    "influencer": {
                        "id": (
                            ad_request.requested_by.id
                            if ad_request.requested_by
                            else ad_request.requested_to.id
                        ),
                        "name": (
                            ad_request.requested_by.name
                            if ad_request.requested_by
                            else ad_request.requested_to.name
                        ),
                        "flagged": (
                            ad_request.requested_by.flagged
                            if ad_request.requested_by
                            else ad_request.requested_to.flagged
                        ),
                        "website": (
                            ad_request.requested_by.website
                            if ad_request.requested_by
                            else ad_request.requested_to.website
                        ),
                        "niche": (
                            ad_request.requested_by.niche
                            if ad_request.requested_by
                            else ad_request.requested_to.niche
                        ),
                        "audience_size": (
                            ad_request.requested_by.audience_size
                            if ad_request.requested_by
                            else ad_request.requested_to.audience_size
                        ),
                        "platforms": [
                            {
                                "platform": platform.platform,
                                "username": platform.username,
                                "url": platform.url,
                                "followers": platform.followers,
                            }
                            for platform in (
                                ad_request.requested_by.platforms
                                if ad_request.requested_by
                                else ad_request.requested_to.platforms
                            )
                        ],
                        "received": (True if ad_request.requested_by else False),
                    },
                }
            )

        print(new_ad_requests_data)
        return render_template(
            "dashboard/sponsor.html",
            campaigns=campaigns_data,
            new_ad_requests=new_ad_requests_data,
        )

    campaigns = db.session.execute(
        db.select(AdRequest)
        .join(Campaign)
        .where(
            (Campaign.end_date > datetime.now()),
            (AdRequest.influencer_id == current_user.id)
            | (AdRequest.requested_by_id == current_user.id)
            | (AdRequest.requested_to_id == current_user.id),
        )
    ).scalars()

    campaigns_data = []

    new_ad_requests_data = []

    for request in campaigns:
        if request.status.name == AdRequestStatus.ACCEPTED.name:
            campaigns_data.append(
                {
                    "id": request.id,
                    "title": request.title,
                    "description": request.description,
                    "start_date": datetime.strftime(
                        request.campaign.start_date, "%Y-%m-%d"
                    ),
                    "end_date": datetime.strftime(
                        request.campaign.end_date, "%Y-%m-%d"
                    ),
                    "payment_amount": request.payment_amount,
                    "niche": request.campaign.niche,
                    "requirements": request.requirements,
                    "flagged": request.campaign.flagged,
                    "sponsor": {
                        "id": request.campaign.user.id,
                        "name": request.campaign.user.name,
                        "website": request.campaign.user.website,
                        "company_name": request.campaign.user.company_name,
                    },
                }
            )
        else:
            new_ad_requests_data.append(
                {
                    "id": request.id,
                    "title": request.title,
                    "description": request.description,
                    "niche": request.campaign.niche,
                    "campaign": request.campaign.title,
                    "campaign_id": request.campaign.id,
                    "payment_amount": request.payment_amount,
                    "requirements": request.requirements,
                    "flagged": request.campaign.flagged,
                    "sponsor": {
                        "id": request.campaign.user.id,
                        "name": request.campaign.user.name,
                        "website": request.campaign.user.website,
                        "company_name": request.campaign.user.company_name,
                    },
                    "received": (
                        True if request.requested_to_id == current_user.id else False
                    ),
                }
            )
    return render_template(
        "dashboard/influencer.html",
        campaigns=campaigns_data,
        new_ad_requests=new_ad_requests_data,
    )


@main.route("/stats")
def stats():
    """Render the statistics page."""

    if current_user.role in (UserRole.ADMIN, UserRole.SUPERADMIN):

        users = db.session.execute(db.select(User).order_by(User.id)).scalars()
        users_data = []
        for user in users:
            users_data.append(
                {
                    "id": user.id,
                    "name": user.name,
                    "role": user.role.name,
                    "flagged": user.flagged,
                }
            )
        user_distribution_by_role = {
            "admin": len(
                [
                    user
                    for user in users_data
                    if user["role"] in (UserRole.ADMIN.name, UserRole.SUPERADMIN.name)
                ]
            ),
            "sponsor": len(
                [user for user in users_data if user["role"] == UserRole.SPONSOR.name]
            ),
            "influencer": len(
                [
                    user
                    for user in users_data
                    if user["role"] == UserRole.INFLUENCER.name
                ]
            ),
        }

        user_distribution_by_flagged_status = {
            "flagged": len([user for user in users_data if user["flagged"]]),
            "not_flagged": len([user for user in users_data if not user["flagged"]]),
        }

        campaigns = db.session.execute(
            db.select(Campaign).order_by(Campaign.id)
        ).scalars()
        campaigns_data = []
        for campaign in campaigns:
            campaigns_data.append(
                {
                    "id": campaign.id,
                    "title": campaign.title,
                    "visibility": campaign.visibility.name,
                    "flagged": campaign.flagged,
                    "sponsor_id": campaign.sponsor_id,
                    "sponsor": campaign.user.name,
                }
            )

        campaign_distribution_by_visibility = {
            "public": len(
                [
                    campaign
                    for campaign in campaigns_data
                    if campaign["visibility"] == CampaignVisibility.PUBLIC.name
                ]
            ),
            "private": len(
                [
                    campaign
                    for campaign in campaigns_data
                    if campaign["visibility"] == CampaignVisibility.PRIVATE.name
                ]
            ),
        }

        campaign_distribution_by_flagged_status = {
            "flagged": len(
                [campaign for campaign in campaigns_data if campaign["flagged"]]
            ),
            "not_flagged": len(
                [campaign for campaign in campaigns_data if not campaign["flagged"]]
            ),
        }

        campaign_distribution_by_sponsor = {}
        for campaign in campaigns_data:
            sponsor_id = str(campaign["sponsor_id"]) + "-" + campaign["sponsor"]
            if sponsor_id not in campaign_distribution_by_sponsor:
                campaign_distribution_by_sponsor[sponsor_id] = 0
            campaign_distribution_by_sponsor[sponsor_id] += 1

        ad_requests = db.session.execute(
            db.select(AdRequest).order_by(AdRequest.id)
        ).scalars()

        ad_requests_data = []
        for ad_request in ad_requests:
            ad_requests_data.append(
                {
                    "id": ad_request.id,
                    "status": ad_request.status.name,
                    "campaign_id": ad_request.campaign_id,
                    "influencer_id": ad_request.influencer_id or "N/A",
                    "influencer": (
                        ad_request.influencer.name
                        if ad_request.influencer
                        else "No Influencer"
                    ),
                }
            )

        ad_request_distribution_by_influencer = {}
        for ad_request in ad_requests_data:
            influencer_id = (
                str(ad_request["influencer_id"]) + "-" + ad_request["influencer"]
            )
            if influencer_id not in ad_request_distribution_by_influencer:
                ad_request_distribution_by_influencer[influencer_id] = 0
            ad_request_distribution_by_influencer[influencer_id] += 1

        return render_template(
            "stats/admin.html",
            user_distribution_by_role=user_distribution_by_role,
            user_distribution_by_flagged_status=user_distribution_by_flagged_status,
            campaign_distribution_by_visibility=campaign_distribution_by_visibility,
            campaign_distribution_by_flagged_status=campaign_distribution_by_flagged_status,
            campaign_distribution_by_sponsor=campaign_distribution_by_sponsor,
            ad_request_distribution_by_influencer=ad_request_distribution_by_influencer,
        )

    if current_user.role == UserRole.SPONSOR:
        campaigns = db.session.execute(
            db.select(Campaign).where(Campaign.sponsor_id == current_user.id)
        ).scalars()

        campaigns_data = []
        for campaign in campaigns:
            campaigns_data.append(
                {
                    "id": campaign.id,
                    "title": campaign.title,
                    "visibility": campaign.visibility.name,
                    "flagged": campaign.flagged,
                }
            )

        campaign_distribution_by_visibility = {
            "public": len(
                [
                    campaign
                    for campaign in campaigns_data
                    if campaign["visibility"] == CampaignVisibility.PUBLIC.name
                ]
            ),
            "private": len(
                [
                    campaign
                    for campaign in campaigns_data
                    if campaign["visibility"] == CampaignVisibility.PRIVATE.name
                ]
            ),
        }

        campaign_distribution_by_flagged_status = {
            "flagged": len(
                [campaign for campaign in campaigns_data if campaign["flagged"]]
            ),
            "not_flagged": len(
                [campaign for campaign in campaigns_data if not campaign["flagged"]]
            ),
        }

        ad_requests = db.session.execute(
            db.select(AdRequest)
            .join(AdRequest.campaign)
            .where(Campaign.sponsor_id == current_user.id)
        ).scalars()

        ad_requests_data = []

        for ad_request in ad_requests:
            ad_requests_data.append(
                {
                    "id": ad_request.id,
                    "status": ad_request.status.name,
                    "campaign_id": ad_request.campaign_id,
                    "influencer_id": ad_request.influencer_id or "N/A",
                    "influencer": (
                        ad_request.influencer.name
                        if ad_request.influencer
                        else "No Influencer"
                    ),
                }
            )

        ad_request_distribution_by_influencer = {}
        for ad_request in ad_requests_data:
            influencer_id = (
                str(ad_request["influencer_id"]) + "-" + ad_request["influencer"]
            )
            if influencer_id not in ad_request_distribution_by_influencer:
                ad_request_distribution_by_influencer[influencer_id] = 0
            ad_request_distribution_by_influencer[influencer_id] += 1

        return render_template(
            "stats/sponsor.html",
            campaign_distribution_by_visibility=campaign_distribution_by_visibility,
            campaign_distribution_by_flagged_status=campaign_distribution_by_flagged_status,
            ad_request_distribution_by_influencer=ad_request_distribution_by_influencer,
        )

    ad_requests = db.session.execute(
        db.select(AdRequest).where(AdRequest.influencer_id == current_user.id)
    ).scalars()

    ad_requests_data = []

    earning = 0

    for ad_request in ad_requests:
        if ad_request.status.name == AdRequestStatus.ACCEPTED.name:
            earning += ad_request.payment_amount
        ad_requests_data.append(
            {
                "id": ad_request.id,
                "status": ad_request.status.name,
                "campaign_id": ad_request.campaign_id,
                "sponsor_id": ad_request.campaign.sponsor_id,
                "sponsor": ad_request.campaign.user.name,
            }
        )

    ad_request_distribution_by_sponsor = {}
    for ad_request in ad_requests_data:
        sponsor_id = str(ad_request["sponsor_id"]) + "-" + ad_request["sponsor"]
        if sponsor_id not in ad_request_distribution_by_sponsor:
            ad_request_distribution_by_sponsor[sponsor_id] = 0
        ad_request_distribution_by_sponsor[sponsor_id] += 1

    return render_template(
        "stats/influencer.html",
        earning=earning,
        ad_request_distribution_by_sponsor=ad_request_distribution_by_sponsor,
    )
