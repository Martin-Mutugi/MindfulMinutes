from backend.extensions import db

user_badges = db.Table('user_badges',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),  # 🔧 Fixed table name
    db.Column('badge_id', db.Integer, db.ForeignKey('badge.id'))
)

class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256))
    icon_url = db.Column(db.String(256))
    users = db.relationship('User', secondary=user_badges, back_populates='badges')
