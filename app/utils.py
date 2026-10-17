import secrets
import string
from urllib.parse import urlparse

from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Link

ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 6
MAX_ATTEMPTS = 5
# Short codes that would clash with real routes.
RESERVED = {"login", "logout", "signup", "dashboard", "static", "links"}


def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def generate_code(length=CODE_LENGTH):
    return "".join(secrets.choice(ALPHABET) for _ in range(length))


def create_link(original_url, user):
    """Create a link with a random unique code.

    The unique constraint on short_code is the real guarantee; the retry loop
    handles the rare case where two requests pick the same code.
    """
    for _ in range(MAX_ATTEMPTS):
        code = generate_code()
        if code.lower() in RESERVED:
            continue
        link = Link(original_url=original_url, short_code=code, owner=user)
        db.session.add(link)
        try:
            db.session.commit()
            return link
        except IntegrityError:
            db.session.rollback()
    return None
