from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from backend.models import JournalEntry, MeditationSession, Meditation
from backend.extensions import db
from backend.services.recommendation_engine import get_user_recommendations, get_daily_recommendation
from datetime import datetime, timedelta

api_bp = Blueprint('api', __name__)

@api_bp.route('/journal/entries', methods=['GET'])
@login_required
def get_journal_entries():
    """
    Get user's journal entries with pagination
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    entries = JournalEntry.query.filter_by(user_id=current_user.id)\
        .order_by(JournalEntry.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'entries': [{
            'id': entry.id,
            'title': entry.title,
            'content': entry.content,
            'mood': entry.mood,
            'sentiment_score': entry.sentiment_score,
            'created_at': entry.created_at.isoformat()
        } for entry in entries.items],
        'total': entries.total,
        'pages': entries.pages,
        'current_page': page
    })

@api_bp.route('/meditation/sessions', methods=['GET'])
@login_required
def get_meditation_sessions():
    """
    Get user's meditation sessions with pagination
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    sessions = MeditationSession.query.filter_by(user_id=current_user.id)\
        .order_by(MeditationSession.started_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'sessions': [{
            'id': session.id,
            'meditation_id': session.meditation_id,
            'duration': session.duration,
            'completed': session.completed,
            'started_at': session.started_at.isoformat() if session.started_at else None,
            'ended_at': session.ended_at.isoformat() if session.ended_at else None
        } for session in sessions.items],
        'total': sessions.total,
        'pages': sessions.pages,
        'current_page': page
    })

@api_bp.route('/recommendations', methods=['GET'])
@login_required
def get_recommendations():
    """
    Get personalized meditation recommendations
    """
    limit = request.args.get('limit', 5, type=int)
    recommendations = get_user_recommendations(current_user.id, limit)
    
    return jsonify({
        'recommendations': [{
            'id': med.id,
            'title': med.title,
            'description': med.description,
            'duration': med.duration,
            'category': med.category,
            'level': med.level,
            'image_url': med.image_url,
            'audio_url': med.audio_url
        } for med in recommendations]
    })

@api_bp.route('/stats/overview', methods=['GET'])
@login_required
def get_stats_overview():
    """
    Get user statistics overview
    """
    # Total meditation time
    total_meditation = MeditationSession.query.filter_by(
        user_id=current_user.id, completed=True
    ).with_entities(db.func.sum(MeditationSession.duration)).scalar() or 0
    
    # Journal entries count
    journal_count = JournalEntry.query.filter_by(user_id=current_user.id).count()
    
    # Current streak
    streak = calculate_streak(current_user.id)
    
    # Weekly average
    week_ago = datetime.utcnow() - timedelta(days=7)
    weekly_avg = MeditationSession.query.filter(
        MeditationSession.user_id == current_user.id,
        MeditationSession.started_at >= week_ago,
        MeditationSession.completed == True
    ).with_entities(db.func.avg(MeditationSession.duration)).scalar() or 0
    
    return jsonify({
        'total_meditation_minutes': total_meditation // 60,
        'journal_entries_count': journal_count,
        'current_streak': streak,
        'weekly_avg_minutes': weekly_avg // 60
    })

@api_bp.route('/mood/trends', methods=['GET'])
@login_required
def get_mood_trends():
    """
    Get mood trends data for charts
    """
    days = request.args.get('days', 30, type=int)
    start_date = datetime.utcnow() - timedelta(days=days)
    
    entries = JournalEntry.query.filter(
        JournalEntry.user_id == current_user.id,
        JournalEntry.created_at >= start_date,
        JournalEntry.mood.isnot(None)
    ).order_by(JournalEntry.created_at).all()
    
    # Group by date and mood
    mood_data = {}
    for entry in entries:
        date_str = entry.created_at.strftime('%Y-%m-%d')
        if date_str not in mood_data:
            mood_data[date_str] = {}
        if entry.mood not in mood_data[date_str]:
            mood_data[date_str][entry.mood] = 0
        mood_data[date_str][entry.mood] += 1
    
    return jsonify({
        'mood_data': mood_data,
        'timeframe': f'last_{days}_days'
    })

def calculate_streak(user_id):
    """Calculate meditation streak"""
    sessions = MeditationSession.query.filter_by(
        user_id=user_id, completed=True
    ).with_entities(
        db.func.date(MeditationSession.started_at).label('session_date')
    ).distinct().order_by('session_date desc').all()
    
    if not sessions:
        return 0
    
    streak = 0
    today = datetime.utcnow().date()
    current_date = today
    
    session_dates = {session.session_date for session in sessions}
    
    while current_date in session_dates:
        streak += 1
        current_date -= timedelta(days=1)
    
    return streak