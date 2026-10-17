from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager


def _now():
    return datetime.now(timezone.utc)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=_now)
    links = db.relationship(
        "Link", backref="owner", lazy="dynamic", cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.Text, nullable=False)
    short_code = db.Column(db.String(16), unique=True, nullable=False, index=True)
    clicks = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=_now)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
