from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from backend.extensions import db
from backend.models import MeditationSession, Meditation
from datetime import datetime

meditation_bp = Blueprint('meditation', __name__, url_prefix='/meditations')

# 🔁 Default redirect to mood-based recommendations
@meditation_bp.route('/')
@login_required
def index():
    return redirect(url_for('meditation.recommend'))

# 🧘 Mood-based recommendations
@meditation_bp.route('/recommend')
@login_required
def recommend():
    # Fallback to 'neutral' if no mood is set
    latest_mood = getattr(current_user, 'latest_journal_mood', 'neutral')

    query = Meditation.query.filter_by(mood_tag=latest_mood)

    # Free users only see non-premium meditations
    if not current_user.is_premium:
        query = query.filter_by(is_premium=False)

    meditations = query.all()
    return render_template("meditation/recommend.html", meditations=meditations, mood=latest_mood)

# 📚 Full meditation library
@meditation_bp.route('/all')
@login_required
def all_meditations():
    query = Meditation.query

    # Free users only see non-premium meditations
    if not current_user.is_premium:
        query = query.filter_by(is_premium=False)

    meditations = query.order_by(Meditation.mood_tag.asc()).all()
    return render_template("meditation/list.html", meditations=meditations)

# 🎧 Individual meditation session (user-specific log)
@meditation_bp.route('/session/<int:id>')
@login_required
def session(id):
    meditation = MeditationSession.query.get_or_404(id)
    return render_template('meditation/session.html', meditation=meditation)

# ✅ Mark session as completed
@meditation_bp.route('/complete/<int:id>', methods=['POST'])
@login_required
def complete(id):
    meditation = MeditationSession.query.get_or_404(id)
    meditation.completed_at = datetime.utcnow()
    db.session.commit()

    flash("Meditation marked as completed.", "success")
    return redirect(url_for('journal.index'))
