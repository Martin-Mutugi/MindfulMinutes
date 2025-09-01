import pytest
from flask import url_for
from backend.models import User
from backend.extensions import db

def test_register_client(client, app):
    """
    Test user registration
    """
    with app.app_context():
        response = client.post(url_for('auth.register'), data={
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Registration successful' in response.data
        
        # Verify user was created in database
        user = User.query.filter_by(email='test@example.com').first()
        assert user is not None
        assert user.username == 'testuser'
        assert user.check_password('password123')

def test_login_client(client, app):
    """
    Test user login
    """
    # First create a test user
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
    
    # Test login
    response = client.post(url_for('auth.login'), data={
        'email': 'test@example.com',
        'password': 'password123',
        'remember_me': True
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Login successful' in response.data
    assert b'Dashboard' in response.data

def test_login_invalid_credentials(client, app):
    """
    Test login with invalid credentials
    """
    response = client.post(url_for('auth.login'), data={
        'email': 'wrong@example.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Invalid email or password' in response.data

def test_logout(client, auth):
    """
    Test user logout
    """
    auth.login()
    
    response = client.get(url_for('auth.logout'), follow_redirects=True)
    
    assert response.status_code == 200
    assert b'You have been logged out' in response.data

def test_protected_route_unauthenticated(client):
    """
    Test that protected routes redirect unauthenticated users
    """
    response = client.get(url_for('main.dashboard'), follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Login' in response.data  # Should redirect to login page

def test_protected_route_authenticated(client, auth):
    """
    Test that authenticated users can access protected routes
    """
    auth.login()
    
    response = client.get(url_for('main.dashboard'))
    
    assert response.status_code == 200
    assert b'Dashboard' in response.data

@pytest.fixture
def auth(client):
    """
    Authentication helper fixture
    """
    class AuthActions:
        def __init__(self, client):
            self._client = client
        
        def login(self, email='test@example.com', password='password123'):
            # Create test user first if needed
            with client.application.app_context():
                user = User.query.filter_by(email=email).first()
                if not user:
                    user = User(
                        username='testuser',
                        email=email,
                        first_name='Test',
                        last_name='User'
                    )
                    user.set_password(password)
                    db.session.add(user)
                    db.session.commit()
            
            return self._client.post(url_for('auth.login'), data={
                'email': email,
                'password': password
            }, follow_redirects=True)
        
        def logout(self):
            return self._client.get(url_for('auth.logout'), follow_redirects=True)
    
    return AuthActions(client)