from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired


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
        validators=[InputRequired()
                    ]
    )

    first_name = StringField(
        "First name",
        validators=[InputRequired()]
    )

    last_name = StringField(
        "Last name",
        validators=[InputRequired()]
    )


class LoginForm(FlaskForm):
    """Form for logging in a user"""

    username = StringField(
        "Username",
        validators=[InputRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired()]
    )


class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""

