from flask import (Blueprint, abort, current_app, flash, redirect,
                   render_template, request, url_for)
from flask_login import current_user, login_required

from app import db
from app.models import Link
from app.utils import create_link, is_valid_url

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("index.html")


@bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        if not is_valid_url(url):
            flash("Enter a valid http:// or https:// URL.", "error")
        elif create_link(url, current_user) is None:
            flash("Could not generate a short code. Please try again.", "error")
        else:
            flash("Short link created.", "success")
        return redirect(url_for("main.dashboard"))

    page = request.args.get("page", 1, type=int)
    pagination = current_user.links.order_by(
        Link.created_at.desc(), Link.id.desc()
    ).paginate(
        page=page,
        per_page=current_app.config["LINKS_PER_PAGE"],
        error_out=False,
    )
    return render_template("dashboard.html", pagination=pagination)


@bp.route("/links/<int:link_id>/delete", methods=["POST"])
@login_required
def delete_link(link_id):
    link = db.session.get(Link, link_id)
    # 404 (not 403) so other users' link ids are not revealed.
    if link is None or link.user_id != current_user.id:
        abort(404)
    db.session.delete(link)
    db.session.commit()
    flash("Link deleted.", "success")
    return redirect(url_for("main.dashboard"))


@bp.route("/<string:code>")
def follow(code):
    link = Link.query.filter_by(short_code=code).first_or_404()
    # Atomic increment in SQL, so concurrent clicks are not lost.
    Link.query.filter_by(id=link.id).update({Link.clicks: Link.clicks + 1})
    db.session.commit()
    return redirect(link.original_url, code=302)
