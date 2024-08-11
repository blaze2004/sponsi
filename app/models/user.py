"""User model"""

import os
from enum import Enum
import uuid
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.campaigns import Campaign
from app.utils import db, login_manager


class UserRole(Enum):
    """User roles"""

    SPONSOR = "sponsor"
    INFLUENCER = "influencer"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"  # Only superadmins can create admin users


class PlatformPresence(db.Model):
    """Platform presence model"""

    __tablename__ = "platform_presence"
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200))
    followers = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class User(UserMixin, db.Model):
    """User model"""

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    about = db.Column(db.Text, default="")
    flagged = db.Column(db.Boolean, default=False)
    flagged_reason = db.Column(db.Text, default="")
    onboarded = db.Column(db.Boolean, default=False)
    website = db.Column(db.Text)

    # Sponsor-specific fields
    company_name = db.Column(db.Text)
    industry = db.Column(db.Text)
    campaigns = db.relationship(Campaign, backref="user", lazy=True)

    # Influencer-specific fields
    platforms = db.relationship("PlatformPresence", backref="user", lazy=True)
    niche = db.Column(db.Text)
    audience_size = db.Column(db.Integer)

    def set_password(self, password):
        """Save hashed password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Decode hashed password and check if it matches"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        """String representation of the user"""
        return self.email


@login_manager.user_loader
def load_user(user):
    """Load user by ID"""
    return User.query.get(int(user))


def create_superadmin():
    """Create a superadmin user if it doesn't exist"""
    superadmin = User.query.filter_by(role=UserRole.SUPERADMIN).first()
    if not superadmin:
        superadmin = User(
            name=os.environ.get("SUPERADMIN_NAME", "Superadmin"),
            email=os.environ.get("SUPERADMIN_EMAIL", "superadmin@sponsi.com"),
            role=UserRole.SUPERADMIN,
        )

        password = os.environ.get("SUPERADMIN_PASSWORD", uuid.uuid4().hex)

        print("Creating superadmin user...")
        print("Email:", superadmin.email)
        print("Password:", password)
        superadmin.set_password(password=password)
        db.session.add(superadmin)
        db.session.commit()
        print("Superadmin user created successfully.")
