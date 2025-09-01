from flask import Flask, redirect, url_for
from config import Config
from backend.extensions import db, login_manager, csrf, mail, migrate

def create_app():
    app = Flask(
        __name__,
        template_folder='../frontend/templates',
        static_folder='../frontend/static'
    )
    app.config.from_object(Config)

    # ✅ Ensure models are registered for Alembic
    from backend import models

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from backend.routes.main import main_bp
    from backend.routes.auth import auth_bp
    from backend.routes.journal import journal_bp
    from backend.routes.meditation import meditation_bp
    from backend.routes.dashboard import dashboard_bp
    from backend.routes.subscription import subscription_bp
    from backend.routes.support import support_bp
    from backend.routes.feedback import feedback_bp
    from backend.routes.legal import legal_bp
    from backend.routes.profile import profile_bp
    from backend.routes.webhook import webhook_bp
    from backend.routes.analytics import analytics_bp
    from backend.routes.badges import badges_bp

    app.register_blueprint(profile_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(journal_bp)
    app.register_blueprint(meditation_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(subscription_bp)
    app.register_blueprint(support_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(legal_bp)
    app.register_blueprint(webhook_bp)
    app.register_blueprint(badges_bp)
    app.register_blueprint(analytics_bp)
    from backend.routes import suggestions
    
    app.register_blueprint(suggestions.bp)
    # ✅ Alias /premium to /subscription/plans
    @app.route('/premium')
    def premium_alias():
        return redirect(url_for('subscription.plans'))

    # ✅ Inject current_year globally into all templates
    @app.context_processor
    def inject_year():
        from datetime import datetime
        return {'current_year': datetime.utcnow().year}

    return app
