from backend.extensions import db
from datetime import datetime

class JournalEntry(db.Model):
    __tablename__ = 'journal_entry'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    mood = db.Column(db.String(20))
    sentiment_score = db.Column(db.Float)
    sentiment_label = db.Column(db.String(50))  # ✅ Stores Hugging Face label
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 🔧 Fixed table name
