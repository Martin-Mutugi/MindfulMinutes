from backend.extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'  # 🔧 Must match foreign key in user_badges

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)  # 🔒 Future-proofed for long hashes
    bio = db.Column(db.String(160))
    is_premium = db.Column(db.Boolean, default=False)
    profile_image_url = db.Column(db.String(255), default='/static/images/default-avatar.png')  # 👤 Profile picture
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    badges = db.relationship('Badge', secondary='user_badges', back_populates='users')

    # Relationships
    journal_entries = db.relationship('JournalEntry', backref='author', lazy=True, cascade="all, delete-orphan")
    meditations = db.relationship('MeditationSession', backref='user', lazy=True, cascade="all, delete-orphan")
    feedback = db.relationship('Feedback', backref='user', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email} | Premium: {self.is_premium}>"
