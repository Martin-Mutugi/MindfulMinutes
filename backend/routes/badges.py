from flask import Blueprint, render_template, session, redirect, url_for
from flask_login import login_required, current_user
from backend.extensions import db
from backend.models import Badge  # Assuming you have a Badge model

badges_bp = Blueprint('badges', __name__, url_prefix='/badges')

@badges_bp.route('/', endpoint='index')
@login_required
def index():
    badges = Badge.query.all()
    session.pop('new_badge', None)  # Clear animation trigger
    return render_template('badges/index.html', badges=badges)

@badges_bp.route('/unlock/<int:badge_id>', endpoint='unlock')
@login_required
def unlock_badge(badge_id):
    badge = Badge.query.get_or_404(badge_id)

    if badge not in current_user.badges:
        current_user.badges.append(badge)
        db.session.commit()
        session['new_badge'] = badge.id  # Trigger animation

    return redirect(url_for('badges.index'))
