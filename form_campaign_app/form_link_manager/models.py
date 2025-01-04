from form_campaign_app import db
from datetime import datetime, timezone, timedelta


class FormLink(db.Model):
    __tablename__ = "form_link"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(10))
    created_time = db.Column(
        db.DateTime, default=datetime.now(timezone(timedelta(hours=7)))
    )
    viewed_time = db.Column(db.DateTime)
    submitted_time = db.Column(db.DateTime)
    uuid = db.Column(db.String(36))

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "created_time": self.created_time,
            "viewed_time": self.viewed_time,
            "submitted_time": self.submitted_time,
            "uuid": self.uuid,
        }
