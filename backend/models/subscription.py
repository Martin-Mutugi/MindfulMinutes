from backend.extensions import db
from datetime import datetime

class Subscription(db.Model):
    __tablename__ = 'subscription'

    id = db.Column(db.Integer, primary_key=True)
    plan_name = db.Column(db.String(50))
    status = db.Column(db.String(20))  # active, cancelled, expired
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 🔧 Fixed table name
