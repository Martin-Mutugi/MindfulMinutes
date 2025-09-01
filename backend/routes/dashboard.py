from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from backend.extensions import db
from backend.models import JournalEntry, MeditationSession
from sqlalchemy import func
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    # Month filter
    selected_month = request.args.get('month') or datetime.now().strftime('%Y-%m')
    selected_year, selected_month_num = map(int, selected_month.split('-'))
    current_month_label = datetime(selected_year, selected_month_num, 1).strftime('%B %Y')
    month_input_value = f"{selected_year}-{str(selected_month_num).zfill(2)}"

    # Journal entries for selected month
    entries = JournalEntry.query.filter(
        JournalEntry.user_id == current_user.id,
        func.extract('year', JournalEntry.created_at) == selected_year,
        func.extract('month', JournalEntry.created_at) == selected_month_num
    ).all()

    # Meditation sessions for selected month
    session_query = MeditationSession.query.filter(
        MeditationSession.user_id == current_user.id,
        MeditationSession.completed_at.isnot(None),
        func.extract('year', MeditationSession.completed_at) == selected_year,
        func.extract('month', MeditationSession.completed_at) == selected_month_num
    )

    if not current_user.is_premium:
        session_query = session_query.filter(MeditationSession.tier == 'free')

    sessions = session_query.all()

    # Mood score
    mood_score = round(
        sum(e.sentiment_score for e in entries) / max(1, len(entries)), 2
    )

    # Mood counts
    raw_mood_counts = db.session.query(
        JournalEntry.mood, func.count(JournalEntry.id)
    ).filter(
        JournalEntry.user_id == current_user.id,
        func.extract('year', JournalEntry.created_at) == selected_year,
        func.extract('month', JournalEntry.created_at) == selected_month_num
    ).group_by(JournalEntry.mood).all()

    mood_counts = [(row[0], row[1]) for row in raw_mood_counts]

    # Total minutes meditated
    total_minutes = db.session.query(
        func.sum(MeditationSession.duration)
    ).filter(
        MeditationSession.user_id == current_user.id,
        MeditationSession.completed_at.isnot(None),
        func.extract('year', MeditationSession.completed_at) == selected_year,
        func.extract('month', MeditationSession.completed_at) == selected_month_num
    ).scalar() or 0

    # Mood timeline
    mood_timeline = db.session.query(
        JournalEntry.created_at,
        JournalEntry.mood
    ).filter(
        JournalEntry.user_id == current_user.id,
        func.extract('year', JournalEntry.created_at) == selected_year,
        func.extract('month', JournalEntry.created_at) == selected_month_num
    ).order_by(JournalEntry.created_at.asc()).all()

    mood_timeline_data = [
        {'date': entry.created_at.strftime('%Y-%m-%d'), 'mood': entry.mood}
        for entry in mood_timeline
    ]

    # Streak tracking
    all_entries = JournalEntry.query.filter_by(user_id=current_user.id).all()
    all_sessions = MeditationSession.query.filter(
        MeditationSession.user_id == current_user.id,
        MeditationSession.completed_at.isnot(None)
    ).all()

    entry_dates = sorted({e.created_at.date() for e in all_entries})
    journal_current_streak = 0
    journal_longest_streak = 0
    previous = None
    for date in entry_dates:
        if previous and (date - previous).days == 1:
            journal_current_streak += 1
        else:
            journal_current_streak = 1
        journal_longest_streak = max(journal_longest_streak, journal_current_streak)
        previous = date

    session_dates = sorted({s.completed_at.date() for s in all_sessions})
    current_streak = 0
    longest_streak = 0
    previous = None
    for date in session_dates:
        if previous and (date - previous).days == 1:
            current_streak += 1
        else:
            current_streak = 1
        longest_streak = max(longest_streak, current_streak)
        previous = date

    # Badge logic
    badges = []
    if journal_current_streak >= 3:
        badges.append("🥉 Reflective Rookie")
    if journal_current_streak >= 7:
        badges.append("🥈 Journal Explorer")
    if journal_current_streak >= 30:
        badges.append("🥇 Emotional Champion")

    if current_streak >= 3:
        badges.append("🧘 Mindful Starter")
    if current_streak >= 7:
        badges.append("🧘‍♂️ Calm Pathfinder")
    if current_streak >= 30:
        badges.append("🧘‍♀️ Zen Master")

    # Calendar activity map
    calendar_data = {}
    for entry in entries:
        date_str = entry.created_at.strftime('%Y-%m-%d')
        calendar_data.setdefault(date_str, []).append('📝')

    for session in sessions:
        date_str = session.completed_at.strftime('%Y-%m-%d')
        calendar_data.setdefault(date_str, []).append('🧘')

    # Stats payload
    stats = {
        'entries': len(entries),
        'sessions': len(sessions),
        'mood_score': mood_score,
        'mood_counts': mood_counts,
        'total_minutes': total_minutes,
        'mood_timeline': mood_timeline_data,
        'streaks': {
            'current': current_streak,
            'longest': longest_streak
        },
        'journal_streaks': {
            'current': journal_current_streak,
            'longest': journal_longest_streak
        },
        'badges': badges,
        'calendar': calendar_data,
        'current_month': current_month_label,
        'month_input_value': month_input_value,
        'onboarding': len(entries) == 0 and len(sessions) == 0,
        'is_premium': current_user.is_premium
    }

    return render_template('main/dashboard.html', stats=stats)
