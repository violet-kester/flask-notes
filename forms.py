from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length


class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField(
        "Username",
        validators=[InputRequired(),
                    Length(max=20)]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired(),
                    Length(max=100)]
    )

    email = StringField(
        "E-mail",
        validators=[InputRequired(),
                    Length(max=50)]
    )

    first_name = StringField(
        "First name",
        validators=[InputRequired(),
                    Length(max=30)]
    )

    last_name = StringField(
        "Last name",
        validators=[InputRequired(),
                    Length(max=30)]
    )


class LoginForm(FlaskForm):
    """Form for logging in a user"""

    username = StringField(
        "Username",
        validators=[InputRequired(),
                    Length(max=20)]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired(),
                    Length(max=100)]
    )


class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""


class AddNoteForm(FlaskForm):
    """Form for adding a note."""

    title = StringField(
        "Title",
        validators=[InputRequired(),
                    Length(max=100)]
    )

    content = TextAreaField(
        "Title",
        validators=[InputRequired()]
    )

class UpdateNoteForm(FlaskForm):
    """Form for updating note info."""

    title = StringField(
        "Title",
        validators=[Length(max=100)]
    )

    content = TextAreaField(
        "Title"
    )

