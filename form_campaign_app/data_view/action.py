from flask import jsonify, current_app, send_file, after_this_request
from form_campaign_app import db
from form_campaign_app.data_view.models import Campaign
import traceback
from datetime import datetime, timedelta, timezone
import os
from ..utils.pdf_generator import create_campaign_pdf

class CampaignAction:
    def __init__(self):
        # Define field configurations
        self.fields = {
            'responden_name': {'type': 'str', 'default': ''},
            'campaign_name': {'type': 'str', 'default': ''},
            'start_date': {'type': 'str', 'default': ''},
            'end_date': {'type': 'str', 'default': ''},
            'unit': {'type': 'str', 'default': ''},
            'brand': {'type': 'str', 'default': ''},
            'program': {'type': 'str', 'default': ''},
            'jenis_paket': {'type': 'str', 'default': ''},
            'nilai_paket': {'type': 'float', 'default': 0},
            'revenue_prorate': {'type': 'str', 'default': ''},  # Changed to str
            'total_real_cost': {'type': 'float', 'default': 0},
            'breakdown_cost': {'type': 'str', 'default': ''},
            'breakdown_kpi': {'type': 'str', 'default': ''},
            'activity_type': {'type': 'str', 'default': ''},
            'list_benefit': {'type': 'str', 'default': ''},
            'detail_brief': {'type': 'str', 'default': ''},
            'timeline_benefit': {'type': 'str', 'default': ''},
            'product_knowledge': {'type': 'str', 'default': ''},
            'key_visual_design': {'type': 'str', 'default': ''}
        }

    def _process_field_value(self, field_name, value):
        """Helper method to process field values based on their type"""
        field_config = self.fields[field_name]
        
        if field_config['type'] == 'float':
            try:
                return float(value) if value else field_config['default']
            except (ValueError, TypeError):
                return field_config['default']
        return value if value else field_config['default']

    def _generate_responden_id(self, name):
        """Helper method to generate responden_id"""
        name_parts = name.split()
        initials = ''.join(word[0].upper() for word in name_parts) if name_parts else 'XX'
        current_date = datetime.now(timezone(timedelta(hours=7))).strftime('%d%m%y')
        
        existing_count = Campaign.query.filter(
            Campaign.responden_name.ilike(name)
        ).count()
        
        counter = str(existing_count + 1).zfill(4)
        return f"{counter}{initials}{current_date}"

    def view(self, id):
        try:
            campaign = Campaign.query.get(id)
            if campaign is None:
                return jsonify({'error': f'Campaign with id {id} not found'}), 400
            return jsonify(campaign.to_dict()), 200
        except Exception as e:
            current_app.logger.error(f'Error in view action: {str(e)}\n{traceback.format_exc()}')
            return jsonify({'error': str(e)}), 500

    def edit(self, id, data):
        try:
            campaign = Campaign.query.get(id)
            if campaign is None:
                return jsonify({'error': f'Campaign with id {id} not found'}), 404
            
            # Check if responden_name is being updated
            if 'responden_name' in data and data['responden_name'] != campaign.responden_name:
                # Generate new responden_id based on new name
                new_responden_id = self._generate_responden_id(data['responden_name'])
                campaign.responden_id = new_responden_id
            
            # Update all fields using field configuration
            for field_name in self.fields:
                if field_name in data:  # Only update fields that are provided
                    value = data.get(field_name)
                    processed_value = self._process_field_value(field_name, value)
                    setattr(campaign, field_name, processed_value)
            
            db.session.commit()
            return jsonify({
                'message': 'Campaign updated successfully',
                'data': campaign.to_dict()
            }), 200
            
        except Exception as e:
            db.session.rollback()
            print(f'Error in edit action: {str(e)}\n{traceback.format_exc()}')
            return jsonify({'error': str(e)}), 500

    def add(self, data):
        try:
            # Generate responden_id
            responden_id = self._generate_responden_id(data.get('responden_name', ''))
            
            # Process all fields
            field_values = {
                field_name: self._process_field_value(field_name, data.get(field_name))
                for field_name in self.fields
            }
            
            # Create new campaign
            new_campaign = Campaign(
                responden_id=responden_id,
                entry_time=datetime.now(timezone(timedelta(hours=7))),
                **field_values
            )
            
            db.session.add(new_campaign)
            db.session.commit()

            return jsonify({
                'status': 'success',
                'message': 'Campaign added successfully',
                'data': new_campaign.to_dict(),
            }), 201
            
        except Exception as e:
            db.session.rollback()
            print(f'Error in add action: {str(e)}\n{traceback.format_exc()}')
            return jsonify({'error': str(e)}), 500

    def delete(self, id):
        try:
            campaign = Campaign.query.get(id)
            if campaign is None:
                return jsonify({'error': f'Campaign with id {id} not found'}), 400
            db.session.delete(campaign)
            db.session.commit()
            return jsonify({'message': 'Campaign deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error in delete action: {str(e)}\n{traceback.format_exc()}')
            return jsonify({'error': str(e)}), 500

    def pdf(self, id):
        try:
            campaign = Campaign.query.get(id)
            if campaign is None:
                return jsonify({'error': f'Campaign with id {id} not found'}), 404

            # Format the filename: campaign - [yyyymmdd] - [responden_id] - [campaign name]
            creation_date = datetime.now(timezone(timedelta(hours=7))).strftime('%Y%m%d')
            # Clean campaign name (remove special characters that might cause issues in filenames)
            safe_campaign_name = "".join(c for c in campaign.campaign_name if c.isalnum() or c in (' ', '-', '_')).strip()
            filename = f"campaign-{creation_date}-{campaign.responden_id}-{safe_campaign_name}.pdf"
            
            output_path = os.path.join(current_app.config['PDF_OUTPUT_DIR'], filename)
            
            # Generate PDF
            create_campaign_pdf(campaign.to_dict(), output_path)
            
            # Send file with proper headers
            response = send_file(
                output_path,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=filename,
                headers={
                    'X-Filename': filename  # Simple, direct header
                }
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
            print(f'Error in pdf action: {str(e)}\n{traceback.format_exc()}')
            return jsonify({'error': str(e)}), 500 