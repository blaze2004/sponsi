"""Campaign and AdRequest forms."""

from wtforms import DateField, FloatField, Form, RadioField, StringField, validators

from src.app.models.campaigns import CampaignVisibility


class CreateOrUpdateCampaignForm(Form):
    """Create/Update Campaign Form"""

    title = StringField(
        "Title", validators=[validators.DataRequired(message="Title is required.")]
    )
    description = StringField(
        "Description",
        validators=[validators.DataRequired(message="Description is required.")],
    )
    budget = FloatField(
        "Budget",
        validators=[
            validators.DataRequired(message="Budget is required."),
            validators.NumberRange(min=10, message="Budget must be at least ₹10"),
        ],
    )
    start_date = DateField(
        "Start Date",
        validators=[validators.DataRequired(message="Start Date is required.")],
    )
    end_date = DateField(
        "End Date",
        validators=[validators.DataRequired(message="End Date is required.")],
    )

    visibility = RadioField(
        "Visibility",
        choices=[
            (visibility.value, visibility.name) for visibility in CampaignVisibility
        ],
        validators=[
            validators.DataRequired(message="Visibility is required."),
            validators.AnyOf(
                [visibility.value for visibility in CampaignVisibility],
                message="Invalid role.",
            ),
        ],
    )

    niche = StringField(
        "Niche", validators=[validators.DataRequired(message="Niche is required.")]
    )
    goals = StringField(
        "Goals", validators=[validators.DataRequired(message="Goals is required.")]
    )


class CreateOrUpdateAdRequestsForm(Form):
    """Create/Update Ad Request Form"""

    title = StringField(
        "Title", validators=[validators.DataRequired(message="Title is required.")]
    )
    description = StringField(
        "Description",
        validators=[validators.DataRequired(message="Description is required.")],
    )
    payment_amount = FloatField(
        "Payment Amount",
        validators=[
            validators.DataRequired(message="Payment Amount is required."),
            validators.NumberRange(
                min=10, message="Payment Amount must be at least ₹10"
            ),
        ],
    )

    requirements = StringField(
        "Requirements",
        validators=[validators.DataRequired(message="Requirements is required.")],
    )
