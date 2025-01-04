import csv
from datetime import datetime, timezone, timedelta
import traceback

from flask import request
from form_campaign_app import db
from form_campaign_app.log_history.models import LogHistory


class LogHistoryAction:
    def __init__(self):
        self.fields = {
            "id": {"type": "int", "default": 0},
            "timestamp": {"type": "str", "default": ""},
            "ip_address": {"type": "str", "default": ""},
            "browser": {"type": "str", "default": ""},
            "status": {"type": "str", "default": ""},
            "error_message": {"type": "str", "default": ""},
            "category": {"type": "str", "default": ""},
            "action": {"type": "str", "default": ""},
            "details": {"type": "str", "default": ""},
        }

        self.statuses = {
            "success": "Success",
            "warning": "Warning",
            "error": "Error",
            "info": "Info",
        }

        self.activities = {
            "guest_activity": "Guest Activity",
            "form_link_manager_activity": "Form Link Manager Activity",
            "campaign_activity": "Campaign Activity",
            "settings_activity": "Settings Activity",
        }

    def get_user_ip_address(self):
        return request.remote_addr

    def get_user_browser(self):
        return request.user_agent.browser

    def get_all(self):
        try:
            log_histories = LogHistory.query.all()
            return [log_history.to_dict() for log_history in log_histories]
        except Exception as e:
            print(
                f"Error getting all log histories: {str(e)}\n{traceback.format_exc()}"
            )
            return []

    def get_by_id(self, id):
        try:
            log_history = LogHistory.query.get(id)
            return log_history.to_dict()
        except Exception as e:
            print(
                f"Error getting log history by id: {str(e)}\n{traceback.format_exc()}"
            )
            return None

    def export_to_csv(self):
        log_histories = self.get_all()
        with open("log_history.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(self.fields.keys())
            for log_history in log_histories:
                writer.writerow([log_history[field] for field in self.fields.keys()])
        return True

    def add(self, status, error_message, category, activity, details):
        try:
            new_log_history = LogHistory(
                ip_address=self.get_user_ip_address(),
                browser=self.get_user_browser(),
                status=self.statuses[status],
                error_message=error_message,
                category=category,
                activity=activity,
                details=details,
            )
            db.session.add(new_log_history)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error adding log history: {str(e)}\n{traceback.format_exc()}")
            return False

    def purge_all_logs(self):
        try:
            db.session.query(LogHistory).delete()
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error purging all logs: {str(e)}\n{traceback.format_exc()}")
            return False
