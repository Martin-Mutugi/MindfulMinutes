from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from backend.models import JournalEntry, MeditationSession
from datetime import datetime, timedelta
from sqlalchemy import func

analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')

@analytics_bp.route('/mood', endpoint='mood')
@login_required
def mood():
    # Get mood data for the last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)

    entries = JournalEntry.query.filter(
        JournalEntry.user_id == current_user.id,
        JournalEntry.created_at >= thirty_days_ago,
        JournalEntry.mood.isnot(None)
    ).order_by(JournalEntry.created_at).all()

    mood_data = [
        {
            'date': entry.created_at.strftime('%Y-%m-%d'),
            'mood': entry.mood,
            'score': entry.sentiment_score
        }
        for entry in entries
    ]

    return render_template('charts/mood_trends.html', mood_data=mood_data)

@analytics_bp.route('/meditation-stats', endpoint='meditation_stats')
@login_required
def meditation_stats():
    # Get meditation statistics for the last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)

    sessions = MeditationSession.query.filter(
        MeditationSession.user_id == current_user.id,
        MeditationSession.started_at >= thirty_days_ago,
        MeditationSession.completed == True
    ).all()

    # Group by day
    daily_stats = {}
    for session in sessions:
        date_str = session.started_at.strftime('%Y-%m-%d')
        daily_stats[date_str] = daily_stats.get(date_str, 0) + session.duration // 60

    stats_data = [{'date': date, 'minutes': minutes} for date, minutes in daily_stats.items()]

    return render_template('charts/meditation_stats.html', stats_data=stats_data)

@analytics_bp.route('/progress', endpoint='progress')
@login_required
def progress():
    # Get overall progress data
    total_meditation = MeditationSession.query.filter_by(
        user_id=current_user.id, completed=True
    ).with_entities(func.sum(MeditationSession.duration)).scalar() or 0
    total_meditation_minutes = total_meditation // 60

    total_entries = JournalEntry.query.filter_by(user_id=current_user.id).count()

    # Weekly average
    week_ago = datetime.utcnow() - timedelta(days=7)
    weekly_avg = MeditationSession.query.filter(
        MeditationSession.user_id == current_user.id,
        MeditationSession.started_at >= week_ago,
        MeditationSession.completed == True
    ).with_entities(func.avg(MeditationSession.duration)).scalar() or 0
    weekly_avg_minutes = weekly_avg // 60

    return render_template('charts/progress.html',
                           total_meditation=total_meditation_minutes,
                           total_entries=total_entries,
                           weekly_avg=weekly_avg_minutes)
