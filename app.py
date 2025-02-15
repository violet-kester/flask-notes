import os

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from models import connect_db, db, User, Note
from forms import (RegisterForm, LoginForm, CSRFProtectForm, AddNoteForm,
    UpdateNoteForm)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///flask_notes")
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


@app.get("/")
def homepage():
    """Homepage. Redirects to register."""

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register():
    """GET: Show register user form
    POST: Register user - produce form & handle form submission."""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()

        session["username"] = user.username

        # on successful login, redirect to secret page
        return redirect(f"/users/{user.username}")

    else:
        return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """GET: Show user login form
    POST: process login"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            # on successful login, redirect to secret page
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Bad username/password combo"]

    return render_template("login.html", form=form)


@app.get("/users/<username>")
def show_user_page(username):
    """If logged in as correct user, display a page with all info about
    user except password"""

    form = CSRFProtectForm()
    is_authorized = session.get("username") == username

    if not is_authorized:
        # flash("You're not authorized!")
        # return redirect("/")
        raise Unauthorized()

    else:
        user = User.query.get_or_404(username)

        return render_template("user.html", user=user, form=form)


@app.post("/logout")
def logout():
    """Log user out if username is in session"""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        # Remove "username" if present, but no errors if it wasn't
        session.pop("username", None)
        return redirect("/login")

    #TODO: display msg to user about why it failed
    return redirect("/")


@app.post("/users/<username>/delete")
def delete_user(username):
    """Delete user account of logged-in user."""

    form = CSRFProtectForm()
    is_authorized = session.get("username") == username

    if not is_authorized:
        # flash("You're not authorized!")
        # return redirect("/")
        raise Unauthorized()

    elif form.validate_on_submit():
        # Remove "username" if present, but no errors if it wasn't
        session.pop("username", None)
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()

        return redirect('/')


@app.route("/users/<username>/notes/add", methods=["GET", "POST"])
def add_note(username):
    """GET: Show form to add note.
    POST: Add note and submit to database if authorized user is logged in."""

    form = AddNoteForm()
    is_authorized = session.get("username") == username

    if not is_authorized:
        # flash("You're not authorized!")
        # return redirect("/")
        raise Unauthorized()

    elif form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note = Note(title=title, content=content, owner=username)
        db.session.add(note)
        db.session.commit()

        # on successful note add, redirect to user page
        return redirect(f"/users/{username}")

    else:
        return render_template("add_note.html", form=form)

@app.route("/notes/<note_id>/update", methods=["GET", "POST"])
def update_note(note_id):
    """GET: Show form to udpate note info.
    POST: Handle form submission and update note in db if authorized user
    is logged in."""

    note = Note.query.get_or_404(note_id)
    form = UpdateNoteForm(obj=note)
    is_authorized = session.get("username") == note.user.username

    if not is_authorized:
        # flash("You're not authorized!")
        # return redirect("/")
        raise Unauthorized()

    elif form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()

        # on successful note update, redirect to user page
        return redirect(f"/users/{note.user.username}")

    else:
        return render_template("update_note.html", form=form)

@app.post("/notes/<note_id>/delete")
def delete_note(note_id):
    """Delete a note if authorized user is logged in"""

    note = Note.query.get_or_404(note_id)
    form = CSRFProtectForm()
    is_authorized = session.get("username") == note.user.username

    if not is_authorized:
        # flash("You're not authorized!")
        # return redirect("/")
        raise Unauthorized()

    elif form.validate_on_submit():
        db.session.delete(note)
        db.session.commit()
        flash(f"{note.title} deleted!")
        return redirect(f"/users/{note.user.username}")





