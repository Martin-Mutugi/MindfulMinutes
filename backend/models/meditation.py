from backend.extensions import db
from datetime import datetime

class MeditationSession(db.Model):
    __tablename__ = 'meditation_session'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    duration = db.Column(db.Integer)  # in minutes
    tier = db.Column(db.String(10), default='free')  # 'free' or 'premium'
    mood_tag = db.Column(db.String(50))  # Used for mood-based recommendations
    image_url = db.Column(db.String(255))  # Visual cue for the session
    audio_url = db.Column(db.String(255))  # Guided audio or soundtrack
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)  # Tracks when session was completed

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 🔧 Fixed table name


class Meditation(db.Model):
    __tablename__ = 'meditation'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    mood_tag = db.Column(db.String(50))  # e.g. "anxious", "grateful"
    is_premium = db.Column(db.Boolean, default=False)
    image_url = db.Column(db.String(255))  # Visual thumbnail
    audio_url = db.Column(db.String(255))  # Audio file or guided track
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
