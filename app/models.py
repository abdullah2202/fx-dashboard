from datetime import datetime
from app import db


class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    bot_id = db.Column(db.String(100), nullable=False, index=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    event_type = db.Column(db.String(20), nullable=False)  # SETUP, ENTRY, EXIT, UPDATE
    details = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'bot_id': self.bot_id,
            'timestamp': self.timestamp.isoformat(),
            'event_type': self.event_type,
            'details': self.details,
            'created_at': self.created_at.isoformat()
        }
