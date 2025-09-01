import pytest
from datetime import datetime, timedelta
from backend.models import User, JournalEntry, MeditationSession, Meditation
from backend.extensions import db

def test_user_model(app):
    """
    Test User model creation and password hashing
    """
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        user.set_password('password123')
        
        db.session.add(user)
        db.session.commit()
        
        # Test retrieval
        retrieved = User.query.filter_by(email='test@example.com').first()
        assert retrieved is not None
        assert retrieved.username == 'testuser'
        assert retrieved.check_password('password123')
        assert not retrieved.check_password('wrongpassword')
        assert retrieved.get_full_name() == 'Test User'

def test_journal_entry_model(app):
    """
    Test JournalEntry model
    """
    with app.app_context():
        # Create user first
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        # Create journal entry
        entry = JournalEntry(
            user_id=user.id,
            title='Test Entry',
            content='This is a test journal entry',
            mood='happy',
            sentiment_score=0.8,
            tags='test, journal'
        )
        
        db.session.add(entry)
        db.session.commit()
        
        # Test retrieval
        retrieved = JournalEntry.query.filter_by(user_id=user.id).first()
        assert retrieved is not None
        assert retrieved.title == 'Test Entry'
        assert retrieved.mood == 'happy'
        assert retrieved.sentiment_score == 0.8

def test_meditation_session_model(app):
    """
    Test MeditationSession model
    """
    with app.app_context():
        # Create user and meditation
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        user.set_password('password123')
        
        meditation = Meditation(
            title='Test Meditation',
            description='A test meditation',
            duration=10,
            audio_url='/audio/test.mp3',
            category='test'
        )
        
        db.session.add_all([user, meditation])
        db.session.commit()
        
        # Create session
        session = MeditationSession(
            user_id=user.id,
            meditation_id=meditation.id,
            duration=600,  # 10 minutes in seconds
            completed=True
        )
        
        db.session.add(session)
        db.session.commit()
        
        # Test retrieval and relationships
        retrieved = MeditationSession.query.filter_by(user_id=user.id).first()
        assert retrieved is not None
        assert retrieved.duration == 600
        assert retrieved.completed == True
        assert retrieved.meditation.title == 'Test Meditation'
        assert retrieved.user.username == 'testuser'

def test_meditation_model(app):
    """
    Test Meditation model
    """
    with app.app_context():
        meditation = Meditation(
            title='Test Meditation',
            description='A test meditation session',
            duration=15,
            audio_url='/audio/test.mp3',
            image_url='/images/test.jpg',
            category='relaxation',
            level='beginner',
            is_premium=False
        )
        
        db.session.add(meditation)
        db.session.commit()
        
        # Test retrieval
        retrieved = Meditation.query.filter_by(title='Test Meditation').first()
        assert retrieved is not None
        assert retrieved.duration == 15
        assert retrieved.category == 'relaxation'
        assert retrieved.level == 'beginner'
        assert not retrieved.is_premium

def test_user_relationships(app):
    """
    Test User model relationships
    """
    with app.app_context():
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        user.set_password('password123')
        
        # Create related objects
        entry = JournalEntry(
            title='Test Entry',
            content='Test content',
            user=user
        )
        
        meditation = Meditation(
            title='Test Meditation',
            duration=10,
            audio_url='/audio/test.mp3'
        )
        
        session = MeditationSession(
            duration=600,
            completed=True,
            user=user,
            meditation=meditation
        )
        
        db.session.add_all([user, entry, meditation, session])
        db.session.commit()
        
        # Test relationships
        assert user.journal_entries.count() == 1
        assert user.meditation_sessions.count() == 1
        assert user.journal_entries.first().title == 'Test Entry'
        assert user.meditation_sessions.first().duration == 600