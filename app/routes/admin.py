from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash, Response, abort
from flask_login import login_user, logout_user, login_required, current_user

from .. import db
from ..models import Owner, Event, Volunteer
from ..export import to_csv_bytes, to_xlsx_bytes

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        owner = Owner.query.filter_by(username=username).first()

        if owner and owner.check_password(password):
            login_user(owner)
            return redirect(url_for("admin.dashboard"))
        error = "Invalid username or password."

    return render_template("login.html", error=error)


@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("admin.login"))


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    events = Event.query.filter_by(owner_id=current_user.id).order_by(Event.date.desc()).all()
    return render_template("dashboard.html", events=events)


@admin_bp.route("/events", methods=["POST"])
@login_required
def create_event():
    name = request.form.get("name", "").strip()
    date_str = request.form.get("date", "").strip()

    if not name or not date_str:
        flash("Event name and date are required.")
        return redirect(url_for("admin.dashboard"))

    try:
        event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        flash("Invalid date format.")
        return redirect(url_for("admin.dashboard"))

    event = Event(
        name=name,
        date=event_date,
        slug=Event.generate_unique_slug(),
        owner_id=current_user.id,
    )
    db.session.add(event)
    db.session.commit()
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/events/<int:event_id>")
@login_required
def event_detail(event_id):
    event = _get_owned_event_or_404(event_id)
    volunteers = Volunteer.query.filter_by(event_id=event.id).order_by(Volunteer.signed_in_at).all()
    return render_template("event_detail.html", event=event, volunteers=volunteers)


@admin_bp.route("/export/<int:event_id>")
@login_required
def export(event_id):
    event = _get_owned_event_or_404(event_id)
    fmt = request.args.get("format", "csv")

    volunteers = [v.to_dict() for v in Volunteer.query.filter_by(event_id=event.id).all()]

    if fmt == "xlsx":
        data = to_xlsx_bytes(volunteers)
        mimetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        filename = f"{event.slug}-signins.xlsx"
    else:
        data = to_csv_bytes(volunteers)
        mimetype = "text/csv"
        filename = f"{event.slug}-signins.csv"

    return Response(
        data,
        mimetype=mimetype,
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


def _get_owned_event_or_404(event_id):
    event = db.session.get(Event, event_id)
    if event is None or event.owner_id != current_user.id:
        abort(404)
    return event
