"""Auth Forms"""

from wtforms import Form, RadioField, StringField, PasswordField, validators
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
        "Password", [validators.DataRequired(message="Password is required.")]
    )
    password2 = PasswordField(
        "Confirm Password", [validators.EqualTo("password", "Passwords must match.")]
    )
