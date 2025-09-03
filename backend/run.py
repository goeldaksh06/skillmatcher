import os
from app import create_app, db
from app.utils.database import init_db, create_sample_data

app = create_app(os.getenv('FLASK_ENV', 'default'))

@app.cli.command()
def init_database():
    """Initialize the database with tables"""
    with app.app_context():
        init_db()

@app.cli.command()
def seed_data():
    """Create sample data for testing"""
    with app.app_context():
        create_sample_data()

if __name__ == '__main__':
    with app.app_context():
        # Initialize database on first run
        init_db()
        # Optionally create sample data
        create_sample_data()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
