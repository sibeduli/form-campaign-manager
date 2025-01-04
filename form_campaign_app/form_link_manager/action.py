import uuid
from flask import jsonify, request
from form_campaign_app import db
from form_campaign_app.form_link_manager.models import FormLink
import traceback
from datetime import datetime, timezone, timedelta
from form_campaign_app.log_history.action import LogHistoryAction


class FormLinkAction:
    def __init__(self):
        self.fields = {
            "id": {"type": "int", "default": 0},
            "name": {"type": "str", "default": ""},
            "url_link": {"type": "str", "default": ""},
            "status": {"type": "str", "default": ""},
            "created_time": {"type": "str", "default": ""},
            "viewed_time": {"type": "str", "default": ""},
            "submitted_time": {"type": "str", "default": ""},
            # 'uuid': {'type': 'str', 'default': ''}, # uuid is hidden on the table
        }

    def get_all(self):
        try:
            form_links = FormLink.query.all()
            for form_link in form_links:
                if form_link.viewed_time is None:
                    form_link.viewed_time = "Not Viewed"
                if form_link.submitted_time is None:
                    form_link.submitted_time = "Not Submitted"
                form_link.url_link = (
                    f"http://{request.host}/guest-form/{form_link.uuid}"
                )
            return [form_link.to_dict() for form_link in form_links]
        except Exception as e:
            print(f"Error getting all form links: {str(e)}\n{traceback.format_exc()}")
            return []

    def get_url_by_id(self, id):
        try:
            form_link = FormLink.query.get(id)
            if form_link is None:
                return None
            field_uuid = form_link.uuid
            url_link = f"http://{request.host}/guest-form/{field_uuid}"
            return url_link
        except Exception as e:
            print(f"Error getting form link by id: {str(e)}\n{traceback.format_exc()}")
            return None

    def delete_by_id(self, id):
        try:
            form_link = FormLink.query.get(id)
            db.session.delete(form_link)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error deleting form link by id: {str(e)}\n{traceback.format_exc()}")
            return False

    def add(self):
        try:
            creation_time = datetime.now(timezone(timedelta(hours=7)))
            field_uuid = creation_time.strftime("%Y%m%d") + str(uuid.uuid4())
            new_form_link = FormLink(
                status="unopened", created_time=creation_time, uuid=field_uuid
            )
            db.session.add(new_form_link)
            db.session.commit()
            return (
                jsonify(
                    {
                        "message": "Form link added successfully",
                        "data": new_form_link.to_dict(),
                    }
                ),
                200,
            )
        except Exception as e:
            db.session.rollback()
            print(f"Error in add action: {str(e)}\n{traceback.format_exc()}")
            return jsonify({"error": str(e)}), 500

    def get_last_form_link(self):
        try:
            form_link = FormLink.query.order_by(FormLink.created_time.desc()).first()
            return form_link.to_dict()
        except Exception as e:
            print(
                f"Error in get_last_form_link action: {str(e)}\n{traceback.format_exc()}"
            )
            return None

    def update_viewed_time(self, id):
        try:
            form_link = FormLink.query.get(id)
            if form_link:  # Check if form_link exists
                form_link.viewed_time = datetime.now(timezone.utc) + timedelta(
                    hours=7
                )  # Convert to GMT+7
                db.session.commit()
                return True
            return False  # Return False if form_link does not exist
        except Exception as e:
            print(f"Error updating viewed time: {str(e)}\n{traceback.format_exc()}")
            return False

    def update_submitted_time(self, id):
        try:
            form_link = FormLink.query.get(id)
            form_link.submitted_time = datetime.now(timezone.utc) + timedelta(
                hours=7
            )  # Convert to GMT+7
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error updating submitted time: {str(e)}\n{traceback.format_exc()}")
            return False

    def get_last_form_link_submitted(self):
        try:
            form_link = (
                FormLink.query.where(FormLink.submitted_time.isnot(None))
                .order_by(FormLink.submitted_time.desc())
                .first()
            )
            if not form_link:
                return None
            return form_link.to_dict()
        except Exception as e:
            print(
                f"Error in get_last_form_link_submitted action: {str(e)}\n{traceback.format_exc()}"
            )
            return None

    def get_last_form_link_viewed(self):
        try:
            form_link = (
                FormLink.query.where(FormLink.viewed_time.isnot(None))
                .order_by(FormLink.viewed_time.desc())
                .first()
            )
            if not form_link:
                return None
            return form_link.to_dict()
        except Exception as e:
            print(
                f"Error in get_last_form_link_viewed action: {str(e)}\n{traceback.format_exc()}"
            )
            return None

    def change_status(self, id, status):
        try:
            log_history_action = LogHistoryAction()
            log_history_action.add(
                status="info",
                error_message="",
                category="change_status",
                activity="form_link_manager_activity",
                details=f"Form link id: {id}, status: {status}",
            )
            form_link = FormLink.query.get(id)
            form_link.status = status
            db.session.commit()
            log_history_action.add(
                status="success",
                error_message="",
                category="change_status",
                activity="form_link_manager_activity",
                details=f"Form link id: {id}, status: {status}",
            )
            return True
        except Exception as e:
            print(f"Error in change_status action: {str(e)}\n{traceback.format_exc()}")
            log_history_action = LogHistoryAction()
            log_history_action.add(
                status="error",
                error_message=str(traceback.format_exc()),
                activity="form_link_manager_activity",
                category="change_status",
                details=f"Form link id: {id}, status: {status}",
            )
            return False

    def get_unopened_form_count(self):
        try:
            unopened_form_count = FormLink.query.filter(
                FormLink.status == "unopened"
            ).count()
            return unopened_form_count
        except Exception as e:
            print(
                f"Error in get_unopened_form_count action: {str(e)}\n{traceback.format_exc()}"
            )
            return 0

    def get_last_form_link_created(self):
        try:
            form_link = FormLink.query.order_by(FormLink.created_time.desc()).first()
            return form_link.to_dict()
        except Exception as e:
            print(
                f"Error in get_last_form_link_created action: {str(e)}\n{traceback.format_exc()}"
            )
            return None
