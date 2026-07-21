import secrets
from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class Owner(UserMixin, db.Model):
    __tablename__ = "owners"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    events = db.relationship("Event", backref="owner", lazy=True)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    slug = db.Column(db.String(32), unique=True, nullable=False, default=lambda: secrets.token_urlsafe(6))
    owner_id = db.Column(db.Integer, db.ForeignKey("owners.id"), nullable=False)

    volunteers = db.relationship(
        "Volunteer", backref="event", lazy=True, cascade="all, delete-orphan"
    )

    @staticmethod
    def generate_unique_slug() -> str:
        """Generate a slug guaranteed not to collide with an existing event."""
        while True:
            candidate = secrets.token_urlsafe(6)
            if not Event.query.filter_by(slug=candidate).first():
                return candidate


class Volunteer(db.Model):
    __tablename__ = "volunteers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    signed_in_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "signed_in_at": self.signed_in_at.strftime("%Y-%m-%d %H:%M:%S") if self.signed_in_at else "",
        }
