import os
import sys
from backend.extensions import db
from backend.app import create_app

def setup_database():
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")
        
        # Insert sample data if needed
        if '--seed' in sys.argv:
            from database.seeds.users import seed_users
            from database.seeds.meditations import seed_meditations
            from database.seeds.journal_entries import seed_journal_entries
            
            print("Seeding database with sample data...")
            seed_users()
            seed_meditations()
            seed_journal_entries()
            print("Database seeded successfully!")

if __name__ == "__main__":
    setup_database()