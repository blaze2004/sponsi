"""Auth Forms"""

from wtforms import (
    FieldList,
    Form,
    FormField,
    IntegerField,
    RadioField,
    StringField,
    PasswordField,
    validators,
)
from app.models.user import UserRole


class SignUpForm(Form):
    """User SignUp Form"""

    name = StringField("name", [validators.DataRequired(message="Name is required.")])
    email = StringField(
        "email",
        [
            validators.email(message="Email is not valid."),
            validators.DataRequired(message="Email is required."),
        ],
    )
    role = RadioField(
        "role",
        choices=[
            (UserRole.SPONSOR.value, UserRole.SPONSOR.name),
            (UserRole.INFLUENCER.value, UserRole.INFLUENCER.name),
        ],
        validators=[
            validators.DataRequired(),
            validators.AnyOf(
                [UserRole.SPONSOR.value, UserRole.INFLUENCER.value],
                message="Invalid role.",
            ),
        ],
    )
    password = PasswordField(
        "Password",
        [
            validators.DataRequired(message="Password is required."),
            validators.Length(
                min=8, message="Password must be at least 8 characters long."
            ),
            validators.Regexp(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$",
                message="Password must contain at least one uppercase letter, one lowercase letter, and one number.",
            ),
        ],
    )
    password2 = PasswordField(
        "Confirm Password", [validators.EqualTo("password", "Passwords must match.")]
    )


class SponsorOnboardingForm(Form):
    """Sponsor Onboarding Form"""

    company_name = StringField(
        "Company Name", [validators.DataRequired(message="Company name is required.")]
    )
    industry = StringField(
        "Industry", [validators.DataRequired(message="Industry is required.")]
    )
    website = StringField("Website", [validators.URL(message="Invalid URL.")])


class PlatformPresenceForm(Form):
    """Platform Presence Form"""

    platform = StringField(
        "Platform", [validators.DataRequired(message="Platform name is required.")]
    )
    username = StringField(
        "Username", [validators.DataRequired(message="Username is required.")]
    )
    url = StringField("Profile Url", [validators.URL(message="Invalid Profile URL.")])
    followers = IntegerField(
        "Followers", [validators.DataRequired(message="Followers count is required.")]
    )


class InfluencerOnboardingForm(Form):
    """Influencer Onboarding Form"""

    niche = StringField(
        "Niche", [validators.DataRequired(message="Niche is required.")]
    )
    platforms = FieldList(
        FormField(
            PlatformPresenceForm,
            label="Platform Presence",
        ),
        min_entries=1,
        validators=[
            validators.DataRequired(
                message="Presence on at least one platform is required."
            )
        ],
    )
    audience_size = IntegerField(
        "Followers", [validators.DataRequired(message="Followers count is required.")]
    )
    website = StringField(
        "Website", [validators.URL(message="Invalid Portfolio website URL.")]
    )


class AdminOnboardingForm(Form):
    """Admin Onboarding Form (Update Password on First Login)"""

    password = PasswordField(
        "Password",
        [
            validators.DataRequired(message="Password is required."),
            validators.Length(
                min=8, message="Password must be at least 8 characters long."
            ),
            validators.Regexp(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$",
                message="Password must contain at least one uppercase letter, one lowercase letter, and one number.",
            ),
        ],
    )
    password2 = PasswordField(
        "Confirm Password", [validators.EqualTo("password", "Passwords must match.")]
    )
