from flask import Blueprint, render_template, request, abort

from .. import db
from ..models import Event, Volunteer
from ..validation import validate_signin

public_bp = Blueprint("public", __name__)


@public_bp.route("/")
def home():
    return render_template("home.html")


@public_bp.route("/signin/<slug>", methods=["GET", "POST"])
def signin(slug):
    event = Event.query.filter_by(slug=slug).first()
    if event is None:
        abort(404)

    errors = []
    if request.method == "POST":
        name = request.form.get("name", "")
        email = request.form.get("email", "")
        phone = request.form.get("phone", "")

        errors = validate_signin(name, email, phone)

        if not errors:
            volunteer = Volunteer(
                name=name.strip(), email=email.strip(), phone=phone.strip(), event=event
            )
            db.session.add(volunteer)
            db.session.commit()
            return render_template("confirmation.html", event=event, name=volunteer.name)

    return render_template("signin.html", event=event, errors=errors)
