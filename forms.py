from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email


class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField(
        "Username",
        validators=[InputRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired()]
    )

    email = StringField(
        "E-mail",
        validators=[InputRequired(),
                    Email()]
    )

    first_name = StringField(
        "First name",
        validators=[InputRequired()]
    )

    last_name = StringField(
        "Last name",
        validators=[InputRequired()]
    )

