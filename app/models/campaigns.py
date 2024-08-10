"""Campaign and AdRequest model"""

from enum import Enum
from datetime import datetime
from app.utils import db


class CampaignVisibility(Enum):
    """Campaign visibility"""

    PUBLIC = "public"
    PRIVATE = "private"


class AdRequestStatus(Enum):
    """Ad request status"""

    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Message(db.Model):
    """Message model"""

    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    ad_request_id = db.Column(
        db.Integer, db.ForeignKey("ad_request.id"), nullable=False
    )

    sender = db.relationship("User", backref="messages", lazy=True)


class Campaign(db.Model):
    """Campaign model"""

    __tablename__ = "campaign"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    visibility = db.Column(
        db.Enum(CampaignVisibility), default=CampaignVisibility.PUBLIC
    )
    niche = db.Column(db.Text, nullable=False)
    goals = db.Column(db.Text, nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self) -> str:
        """String representation of the campaign"""
        return self.title


class AdRequest(db.Model):
    """AdRequest model"""

    __tablename__ = "ad_request"
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id"), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    messages = db.relationship("Message", backref="ad_request", lazy=True)
    requirements = db.Column(db.Text, nullable=False)
    payment_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(
        db.Enum(AdRequestStatus), nullable=False, default=AdRequestStatus.PENDING
    )

    requested_by_id = db.Column(
        db.Integer, db.ForeignKey("user.id")
    )  # Other influencers can request to join the campaign
    requested_to_id = db.Column(
        db.Integer, db.ForeignKey("user.id")
    )  # The sponsor can invite influencer to join the campaign

    requested_by = db.relationship(
        "User", foreign_keys=[requested_by_id], backref="ad_requests_made", lazy=True
    )
    requested_to = db.relationship(
        "User",
        foreign_keys=[requested_to_id],
        backref="ad_requests_received",
        lazy=True,
    )

    campaign = db.relationship("Campaign", backref="ad_request", lazy=True)
    influencer = db.relationship(
        "User",
        foreign_keys=[influencer_id],
        backref="ad_requests_influencer",
        lazy=True,
    )
