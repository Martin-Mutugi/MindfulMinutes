from flask import current_app
from flask_mail import Message
from threading import Thread
from backend.extensions import mail

def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
            current_app.logger.info('Email sent successfully')
        except Exception as e:
            current_app.logger.error(f'Failed to send email: {e}')

def send_email(subject, recipients, body, html=None):
    """
    Send email asynchronously
    """
    app = current_app._get_current_object()
    msg = Message(
        subject=subject,
        recipients=recipients,
        sender=current_app.config['MAIL_USERNAME']
    )
    msg.body = body
    if html:
        msg.html = html
    
    # Send email in background thread
    Thread(target=send_async_email, args=(app, msg)).start()
    return True

def send_welcome_email(user):
    """
    Send welcome email to new user
    """
    subject = "Welcome to Mindful Minutes!"
    body = f"""
    Hi {user.first_name or user.username},
    
    Welcome to Mindful Minutes! We're excited to have you join our community 
    dedicated to mental wellness and mindfulness.
    
    Get started by:
    1. Exploring our meditation library
    2. Writing your first journal entry
    3. Setting up your meditation reminders
    
    If you have any questions, don't hesitate to reach out to our support team.
    
    With gratitude,
    The Mindful Minutes Team
    """
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ text-align: center; padding: 20px 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 10px; }}
            .footer {{ text-align: center; padding: 20px; color: #666; font-size: 14px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Welcome to Mindful Minutes! 🌿</h1>
            </div>
            <div class="content">
                <p>Hi <strong>{user.first_name or user.username}</strong>,</p>
                <p>We're excited to have you join our community dedicated to mental wellness and mindfulness.</p>
                
                <h3>Get Started:</h3>
                <ol>
                    <li>Explore our meditation library</li>
                    <li>Write your first journal entry</li>
                    <li>Set up your meditation reminders</li>
                </ol>
                
                <p>If you have any questions, don't hesitate to reach out to our support team.</p>
                
                <p>With gratitude,<br>The Mindful Minutes Team</p>
            </div>
            <div class="footer">
                <p>© 2024 Mindful Minutes. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(subject, [user.email], body, html)

def send_meditation_reminder(user):
    """
    Send meditation reminder email
    """
    subject = "🌱 Time for your daily mindfulness practice"
    body = f"""
    Hi {user.first_name or user.username},
    
    Just a friendly reminder to take some time for yourself today. 
    Even a few minutes of meditation can make a big difference in your day.
    
    Current streak: {user.get_streak()} days
    Keep up the great work!
    
    The Mindful Minutes Team
    """
    
    return send_email(subject, [user.email], body)

def send_subscription_confirmation(user, plan_type):
    """
    Send subscription confirmation email
    """
    subject = "🎉 Welcome to Mindful Minutes Premium!"
    body = f"""
    Hi {user.first_name or user.username},
    
    Thank you for upgrading to our {plan_type} premium plan! 
    You now have access to all our premium features:
    
    • Unlimited guided meditations
    • Advanced mood analytics
    • Personalized recommendations
    • Exclusive content
    • Priority support
    
    Start exploring your new features today!
    
    The Mindful Minutes Team
    """
    
    return send_email(subject, [user.email], body)