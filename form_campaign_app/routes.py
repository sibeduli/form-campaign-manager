from flask import (
    render_template,
    request,
    Blueprint,
    url_for,
    redirect,
    flash,
    after_this_request,
    session,
    jsonify,
    send_from_directory,
    send_file,
    current_app,
    Response,
)

from form_campaign_app import app
from form_campaign_app.data_view.action import CampaignAction
from form_campaign_app.data_view.models import Campaign
from form_campaign_app.form_link_manager.action import FormLinkAction
from datetime import datetime, timedelta, timezone
from random import choice, randint
import os

from form_campaign_app.form_link_manager.models import FormLink
from form_campaign_app.log_history.action import LogHistoryAction
from .utils.pdf_generator import create_campaign_pdf
import traceback
import csv
from io import StringIO
import json
import time

@app.route('/')
def data_view():
    log_history_action = LogHistoryAction()
    log_history_action.add(
        status='info',
        error_message='',
        category='route_call',
        activity='data_view_activity',
        details='PAGE VISIT DATA VIEW'
    )
    return render_template('data_view.html')

@app.route('/test')
def test():
    return render_template('guest_form.html')

@app.route('/form-link-manager')
def form_link_manager():
    log_history_action = LogHistoryAction()
    log_history_action.add(
        status='info',
        error_message='',
        category='route_call',
        activity='form_link_manager_activity',
        details='PAGE VISIT FORM LINK MANAGER'
    )
    return render_template('form_link_manager.html')

@app.route('/tos')
def terms_of_service():
    log_history_action = LogHistoryAction()
    log_history_action.add(
        status='info',
        error_message='',
        category='route_call',
        activity='terms_of_service_activity',
        details='PAGE VISIT TERMS OF SERVICE'
    )
    return render_template('tos.html')

@app.route('/log-history')
def log_history():
    log_history_action = LogHistoryAction()
    log_history_action.add(
        status='info',
        error_message='',
        category='route_call',
        activity='log_history_activity',
        details='PAGE VISIT LOG HISTORY'
    )
    return render_template('log_history.html')

@app.route('/settings')
def settings():
    log_history_action = LogHistoryAction()
    log_history_action.add(
        status='info',
        error_message='',
        category='route_call',
        activity='settings_activity',
        details='PAGE VISIT SETTINGS'
    )
    return render_template('settings.html')

@app.route('/api/campaign', methods=['POST'])
def add_campaign():
    try:
        log_history_action = LogHistoryAction()
        log_history_action.add(
            status='info',
            error_message='',
            category='api_call',
            activity='campaign_activity',
            details='Add campaign'
        )
        data = request.get_json()
        action = CampaignAction()
        return action.add(data)
        
    except Exception as e:
        log_history_action.add(
            status='error',
            error_message=str(traceback.format_exc()),
            category='api_call',
            activity='campaign_activity',
            details='Add campaign'
        )
        print(f"Error in add_campaign:", str(e))
        return jsonify({'error': str(e)}), 500

def generate_sample_data():
    campaigns = []
    units = ["Unit A", "Unit B", "Unit C", "Unit D"]
    brands = ["Brand X", "Brand Y", "Brand Z"]
    programs = ["Program 1", "Program 2", "Program 3"]
    jenis_pakets = ["Sponsorship", "Advertisement", "Partnership"]
    
    for i in range(1, 101):
        random_date = datetime.now() - timedelta(days=randint(0, 30))
        entry_time = random_date.strftime("%Y-%m-%d %H:%M:%S")
        
        campaigns.append({
            "table_id": i,
            "responden_id": f"R{str(i).zfill(3)}",
            "entry_time": entry_time,
            "responden": f"Responden {i}",
            "unit": choice(units),
            "brand": choice(brands),
            "program": choice(programs),
            "jenis_paket": choice(jenis_pakets),
            "nilai_paket": randint(50000, 500000),
            "revenue_prorate": randint(40000, 400000),
            "total_real_cost": randint(30000, 300000),
            "breakdown_cost": f"Cost breakdown details for campaign {i}",
            "breakdown_kpi": f"KPI breakdown details for campaign {i}",
            "campaign_name": f"Sample Campaign {i}"
        })
    
    return campaigns

@app.route('/api/campaigns', methods=['GET'])
def get_campaigns():
    try:
        log_history_action = LogHistoryAction()
        log_history_action.add(
            status='info',
            error_message='',
            category='api_call',
            activity='campaign_activity',
            details='Get campaigns'
        )
        campaigns = Campaign.query.all()
        campaigns_dict = [campaign.to_dict() for campaign in campaigns]
        return jsonify(campaigns_dict), 200
    except Exception as e:
        log_history_action.add(
            status='error',
            error_message=str(traceback.format_exc()),
            category='api_call',
            activity='campaign_activity',
            details='Get campaigns'
        )
        print(f'Error in get_campaigns: {str(e)}\n{traceback.format_exc()}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/campaigns/action/view/<id>', methods=['GET'])
def view_campaign(id):
    try:
        log_history_action = LogHistoryAction()
        log_history_action.add(
            status='info',
            error_message='',
            category='api_call',
            activity='campaign_activity',
            details='View campaign'
        )
        action = CampaignAction()
        return action.view(id)
    except Exception as e:
        log_history_action.add(
            status='error',
            error_message=str(traceback.format_exc()),
            category='api_call',
            activity='campaign_activity',
            details='View campaign'
        )
        print(f'Error in view_campaign: {str(e)}\n{traceback.format_exc()}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/campaigns/action/edit/<int:id>', methods=['PUT'])
def edit_campaign(id):
    try:
        log_history_action = LogHistoryAction()
        log_history_action.add(
            status='info',
            error_message='',
            category='api_call',
            activity='campaign_activity',
            details='Edit campaign'
        )
        data = request.get_json()
        action = CampaignAction()
        return action.edit(id, data)
    except Exception as e:
        log_history_action.add(
            status='error',
            error_message=str(traceback.format_exc()),
            category='api_call',
            activity='campaign_activity',
            details='Edit campaign'
        )
        print(f"Error in edit_campaign:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/api/campaigns/action/pdf/<id>', methods=['GET'])
def pdf_campaign(id):
    try:
        log_history_action = LogHistoryAction()
        log_history_action.add(
            status='info',
            error_message='',
            category='api_call',
            activity='campaign_activity',
            details='Generate PDF campaign'
        )
        action = CampaignAction()
        campaign = Campaign.query.get(id)
        if campaign is None:
            return jsonify({'error': f'Campaign with id {id} not found'}), 404

        # Format the filename: campaign - [yyyymmdd] - [responden_id] - [campaign name]
        creation_date = datetime.now(timezone(timedelta(hours=7))).strftime('%Y%m%d')
        safe_campaign_name = "".join(c for c in campaign.campaign_name if c.isalnum() or c in (' ', '-', '_')).strip()
        filename = f"campaign-{creation_date}-{campaign.responden_id}-{safe_campaign_name}.pdf"
        
        output_path = os.path.join(current_app.config['PDF_OUTPUT_DIR'], filename)
        
        # Generate PDF
        create_campaign_pdf(campaign.to_dict(), output_path)
        
        # Send file
        response = send_file(
            output_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename  # This will set Content-Disposition header correctly
        )
        
        # Clean up the file after sending
        @after_this_request
        def remove_file(response):
            try:
                os.remove(output_path)
            except Exception as e:
                print(f'Error removing temporary file: {str(e)}')
            return response
        
        return response
        
    except Exception as e:
        log_history_action.add(
            status='error',
            error_message=str(traceback.format_exc()),
            category='api_call',
            activity='campaign_activity',
            details='Generate PDF campaign'
        )
        print(f'Error generating PDF: {str(e)}\n{traceback.format_exc()}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/campaigns/action/delete/<id>', methods=['DELETE'])
def delete_campaign(id):
    try:
        log_history_action = LogHistoryAction()
        log_history_action.add(
            status='info',
            error_message='',
            category='api_call',
            activity='campaign_activity',
                details='Delete campaign'
            )
        action = CampaignAction()
        return action.delete(id)
    except Exception as e:
        log_history_action.add(
            status='error',
            error_message=str(traceback.format_exc()),
            category='api_call',
            activity='campaign_activity',
            details='Delete campaign'
        )
        print(f'Error in delete_campaign: {str(e)}\n{traceback.format_exc()}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/campaigns/export-to-csv', methods=['GET'])
def export_campaigns_to_csv():
    try:
        log_history_action = LogHistoryAction()
        log_history_action.add(
            status='info',
            error_message='',
            category='api_call',
            activity='campaign_activity',
            details='Export campaigns to CSV'
        )
        # Get all campaigns
        campaigns = Campaign.query.all()
        
        # Create a StringIO object to write CSV data
        si = StringIO()
        writer = csv.writer(si)
        
        # Write headers - using the field names from our model
        headers = [
            'Table ID', 'Responden ID', 'Entry Time', 'Responden Name', 
            'Campaign Name', 'Start Date', 'End Date', 'Unit', 'Brand', 
            'Program', 'Jenis Paket', 'Nilai Paket', 'Revenue Prorate',
            'Total Real Cost', 'Breakdown Cost', 'Breakdown KPI',
            'Activity Type', 'List Benefit', 'Detail Brief',
            'Timeline Benefit', 'Product Knowledge', 'Key Visual Design'
        ]
        writer.writerow(headers)
        
        # Write data rows
        for campaign in campaigns:
            writer.writerow([
                campaign.table_id,
                campaign.responden_id,
                campaign.entry_time.strftime('%Y-%m-%d %H:%M:%S'),
                campaign.responden_name,
                campaign.campaign_name,
                campaign.start_date,
                campaign.end_date,
                campaign.unit,
                campaign.brand,
                campaign.program,
                campaign.jenis_paket,
                campaign.nilai_paket,
                campaign.revenue_prorate,
                campaign.total_real_cost,
                campaign.breakdown_cost,
                campaign.breakdown_kpi,
                campaign.activity_type,
                campaign.list_benefit,
                campaign.detail_brief,
                campaign.timeline_benefit,
                campaign.product_knowledge,
                campaign.key_visual_design
            ])
        
        # Create the response
        output = si.getvalue()
        si.close()
        
        # Generate filename with timestamp with trailing milliseconds
        filename = f"campaigns_export_{datetime.now(timezone(timedelta(hours=7))).strftime('%Y%m%d_%H%M%S_%f')}.csv"
        
        return Response(
            output,
            mimetype='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"',
                'Content-Type': 'text/csv'
            }
        )
        
    except Exception as e:
        log_history_action.add(
            status='error',
            error_message=str(traceback.format_exc()),
            category='api_call',
            activity='campaign_activity',
            details='Export campaigns to CSV'
        )
        print(f'Error exporting CSV: {str(e)}\n{traceback.format_exc()}')
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/form-link-manager', methods=['GET'])
def get_form_link_manager():
    try:
        log_history_action = LogHistoryAction()
        log_history_action.add(
            status='info',
            error_message='',
            category='api_call',
            activity='form_link_manager_activity',
            details='Get form link manager'
        )
        action = FormLinkAction()
        return jsonify(action.get_all()), 200
    except Exception as e:
        log_history_action.add(
            status='error',
            error_message=str(traceback.format_exc()),
            category='api_call',
            activity='form_link_manager_activity',
            details='Get form link manager'
        )
        print(f'Error in get_form_link_manager: {str(e)}\n{traceback.format_exc()}')
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/form-link-manager/add', methods=['POST'])
def add_form_link():
    try:
        log_history_action = LogHistoryAction()
        log_history_action.add(
            status='info',
            error_message='',
            category='api_call',
            activity='form_link_manager_activity',
            details='Add form link'
        )
        action = FormLinkAction()
        return action.add()
    except Exception as e:
        log_history_action.add(
            status='error',
            error_message=str(traceback.format_exc()),
            category='api_call',
            activity='form_link_manager_activity',
            details='Add form link'
        )
        print(f'Error in add_form_link: {str(e)}\n{traceback.format_exc()}')
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/form-link-manager/action/delete/<id>', methods=['DELETE'])
def delete_form_link(id):
    try:
        log_history_action = LogHistoryAction()
        log_history_action.add(
            status='info',
            error_message='',
            category='api_call',
            activity='form_link_manager_activity',
            details='Delete form link'
        )
        action = FormLinkAction()
        action.delete_by_id(id)
        log_history_action.add(
            status='success',
            error_message='',
            category='api_call',
            activity='form_link_manager_activity',
            details='Delete form link'
        )
        return jsonify({'message': 'Form link deleted successfully'}), 200
    except Exception as e:
        log_history_action.add(
            status='error',
            error_message=str(traceback.format_exc()),
            category='api_call',
            activity='form_link_manager_activity',
            details='Delete form link'
        )
        print(f'Error in delete_form_link: {str(e)}\n{traceback.format_exc()}')
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/form-link-manager/action/copy/<id>', methods=['POST'])
def copy_form_link(id):
    try:
        log_history_action = LogHistoryAction()
        log_history_action.add(
            status='info',
            error_message='',
            category='api_call',
            activity='form_link_manager_activity',
            details='Copy form link'
        )
        action = FormLinkAction()
        url_link = action.get_url_by_id(id)
        if url_link is None:
            log_history_action.add(
                status='warning',
                error_message='',
                category='api_call',
                activity='form_link_manager_activity',
                details='Copy form link but form link not found'
            )
            return jsonify({'error': 'Form link not found'}), 500
        log_history_action.add(
            status='success',
            error_message='',
            category='api_call',
            activity='form_link_manager_activity',
            details='Copy form link'
        )
        return jsonify({'message': 'Form link copied successfully', 'url_link': url_link}), 200
    except Exception as e:
        log_history_action.add(
            status='error',
            error_message=str(traceback.format_exc()),
            category='api_call',
            activity='form_link_manager_activity',
            details='Copy form link'
        )
        print(f'Error in copy_form_link: {str(e)}\n{traceback.format_exc()}')
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/form-link-manager/action/get-last-form-link', methods=['GET'])
def get_last_form_link():
    try:
        log_history_action = LogHistoryAction()
        log_history_action.add(
            status='info',
            error_message='',
            category='api_call',
            activity='form_link_manager_activity',
            details='Get last form link'
        )
        action = FormLinkAction()
        data = action.get_last_form_link()
        data['url_link'] = f'http://{request.host}/guest-form/{data["uuid"]}'
        log_history_action.add(
            status='success',
            error_message='',
            category='api_call',
            activity='form_link_manager_activity',
            details='Get last form link'
        )
        return jsonify(data), 200
    except Exception as e:
        log_history_action = LogHistoryAction()
        log_history_action.add(
            status='error',
            error_message=str(traceback.format_exc()),
            category='api_call',
            activity='form_link_manager_activity',
            details='Get last form link'
        )
        print(f'Error in get_last_form_link: {str(e)}\n{traceback.format_exc()}')
        return jsonify({'error': str(e)}), 500
    
@app.route('/guest-form/<uuid>')
def guest_form(uuid):
    log_history_action = LogHistoryAction()
    log_history_action.add(
        status='info',
        error_message='',
        category='route_call',
        activity='guest_activity',
        details=f'Guest TRIED to open form with uuid: {uuid}'
    )
    data = FormLink.query.filter_by(uuid=uuid).first()
    action = FormLinkAction()
    if data is None:
        log_history_action.add(
            status='warning',
            error_message='',
            category='route_call',
            activity='guest_activity',
            details=f'Guest TRIED to open form with UNKNOWN uuid: {uuid}'
        )
        return render_template('404.html')
    if data.status == 'submitted':
        log_history_action.add(
            status='warning',
            error_message='',
            category='route_call',
            activity='guest_activity',
            details=f'Guest TRIED to open ALREADY SUBMITTED form with uuid: {uuid}'
        )
        return render_template('guest_success.html', uuid=uuid)
    if data.viewed_time is None:
        action.update_viewed_time(data.id)
        log_history_action.add(
            status='info',
            error_message='',
            category='route_call',
            activity='guest_activity',
            details=f'Guest VIEWED form with uuid: {uuid}'
        )
    action.change_status(data.id, 'viewed')
    return render_template('guest_form.html', uuid=uuid)

@app.route('/guest-status/<uuid>')
def guest_status(uuid):
    log_history_action = LogHistoryAction()
    log_history_action.add(
        status='info',
        error_message='',
        category='route_call',
        activity='guest_activity',
        details=f'Guest TRIED to open form STATUS with uuid: {uuid}'
    )
    data = FormLink.query.filter_by(uuid=uuid).first()
    if data is None:
        log_history_action.add(
            status='warning',
            error_message='',
            category='route_call',
            activity='guest_activity',
            details=f'Guest TRIED to open form STATUS with UNKNOWN uuid: {uuid}'
        )
        return render_template('404.html')
    action = FormLinkAction()
    action.change_status(data.id, 'submitted')
    action.update_submitted_time(data.id)
    log_history_action.add(
        status='success',
        error_message='',
        category='route_call',
        activity='guest_activity',
        details=f'Guest SUBMITTED form with uuid: {uuid}'
    )
    return render_template('guest_success.html', uuid=uuid)

@app.route('/api/form-link-manager/action/get-last-form-link-submitted', methods=['GET'])
def get_last_form_link_submitted():
    try:
        log_history_action = LogHistoryAction()
        log_history_action.add(
            status='info',
            error_message='',
            category='api_call',
            activity='form_link_manager_activity',
            details='Get last form link submitted'
        )
        action = FormLinkAction()
        data = action.get_last_form_link_submitted()
        if data is None:
            return jsonify({'id': '-'}), 200
        return jsonify(data), 200
    except Exception as e:
        log_history_action = LogHistoryAction()
        log_history_action.add(
            status='error',
            error_message=str(traceback.format_exc()),
            category='api_call',
            activity='form_link_manager_activity',
            details='Get last form link submitted'
        )
        print(f'Error in get_last_form_link_submitted: {str(e)}\n{traceback.format_exc()}')
        return jsonify({'error': str(e)}), 500
        

@app.route('/api/form-link-manager/status', methods=['GET'])
def form_link_status():
    def generate():
        while True:
            # Create an application context for this iteration
            with app.app_context():
                action = FormLinkAction()
                last_form_submitted = action.get_last_form_link_submitted()
                last_form_viewed = action.get_last_form_link_viewed()
                unopened_form_count = action.get_unopened_form_count()
                last_form_created = action.get_last_form_link_created()

                data = {
                    'unopened_form_count': unopened_form_count or '0',
                    'last_form_id_created': last_form_created['id'] if last_form_created else '-',
                    'last_form_id_submitted': last_form_submitted['id'] if last_form_submitted else '-',
                    'last_form_id_viewed': last_form_viewed['id'] if last_form_viewed else '-',
                }
                yield f"data: {json.dumps(data)}\n\n"
            time.sleep(5)

    return Response(
        generate(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
        }
    )

@app.route('/api/log-history', methods=['GET'])
def get_log_history():
    action = LogHistoryAction()
    data = action.get_all()
    print(data)
    return jsonify(data), 200

@app.route('/api/server-status')
def server_status():
    def generate():
        while True:
            data = {
                'status': 'online',
                'timestamp': datetime.now(timezone(timedelta(hours=7))).strftime('%Y-%m-%d %H:%M:%S')
            }
            yield f"data: {json.dumps(data)}\n\n"
            # Send heartbeat every 5 seconds
            time.sleep(5)

    return Response(
        generate(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
        }
    )
