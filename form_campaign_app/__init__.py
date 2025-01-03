from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from form_campaign_app.config import Config
import os

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db = SQLAlchemy(app)

# Add to your app configuration
app.config['PDF_OUTPUT_DIR'] = os.path.join(app.root_path, 'static', 'pdfs')

def init_db():
    # Create database file if it doesn't exist
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data.db')
    
    # Import Campaign model to ensure it's registered with SQLAlchemy
    from form_campaign_app.data_view.models import Campaign
    # Import FormLink model to ensure it's registered with SQLAlchemy
    from form_campaign_app.form_link_manager.models import FormLink
    # Import LogHistory model to ensure it's registered with SQLAlchemy
    from form_campaign_app.log_history.models import LogHistory
    
    # Create all database tables based on registered models
    with app.app_context():
        # Check if tables exist by inspecting the database
        inspector = db.inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        if not existing_tables:
            # Only create tables if they don't exist
            db.create_all()
            print(f"Database tables created at {db_path}")
        else:
            print(f"Database already exists at {db_path}")

# Call init_db when the application starts
init_db()

# Import routes after db initialization to avoid circular imports
from form_campaign_app import routes