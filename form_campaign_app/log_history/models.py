from form_campaign_app import db
from datetime import datetime, timezone, timedelta


class LogHistory(db.Model):
    __tablename__ = "log_history"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(
        db.DateTime, default=datetime.now(timezone(timedelta(hours=7)))
    )
    ip_address = db.Column(db.String(15))
    status = db.Column(db.String(10))
    error_message = db.Column(db.Text)
    category = db.Column(db.String(255))
    activity = db.Column(db.String(255))
    details = db.Column(db.Text)
    browser = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "ip_address": self.ip_address,
            "status": self.status,
            "error_message": self.error_message,
            "category": self.category,
            "activity": self.activity,
            "details": self.details,
            "browser": self.browser,
        }
