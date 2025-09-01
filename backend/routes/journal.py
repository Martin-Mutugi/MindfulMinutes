from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from backend.extensions import db
from backend.models import JournalEntry, MeditationSession
from backend.forms import JournalForm
from backend.utils.sentiment import get_sentiment

journal_bp = Blueprint('journal', __name__, url_prefix='/journal')

@journal_bp.route('/')
@login_required
def index():
    mood_filter = request.args.get('mood')
    query = JournalEntry.query.filter_by(user_id=current_user.id)

    if mood_filter:
        query = query.filter_by(mood=mood_filter)

    entries = query.order_by(JournalEntry.created_at.desc()).all()

    # Attach recommended meditation to each entry
    for entry in entries:
        entry.recommended = MeditationSession.query.filter_by(mood_tag=entry.mood).first()

    return render_template('journal/index.html', entries=entries)

@journal_bp.route('/entry', methods=['GET', 'POST'])
@login_required
def entry():
    form = JournalForm()
    if form.validate_on_submit():
        content = form.content.data
        mood = form.mood.data

        # Analyze sentiment using Hugging Face
        label, score = get_sentiment(content)

        # Create and store journal entry
        entry = JournalEntry(
            content=content,
            mood=mood,
            sentiment_score=score,
            sentiment_label=label,
            author=current_user
        )
        db.session.add(entry)
        db.session.commit()

        flash(f"Entry saved. Sentiment: {label} ({round(score, 2)})", "info")
        return redirect(url_for('journal.index'))

    return render_template('journal/entry.html', form=form)

@journal_bp.route('/view/<int:id>')
@login_required
def view(id):
    entry = JournalEntry.query.get_or_404(id)

    # Match meditation based on journal mood
    recommended = MeditationSession.query.filter_by(mood_tag=entry.mood).first()

    return render_template('journal/view.html', entry=entry, recommended=recommended)
