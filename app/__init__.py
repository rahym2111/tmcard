import os
from flask import Flask
from flask_login import current_user
from flask_wtf.csrf import generate_csrf
from app.config import Config
from app.extensions import db, login_manager, csrf
from app.models import User, Business, Product

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # 1. Instance papkasynyň bar bolmagyny üpjün etmek (SQLite ýalňyşlygyny çözýär)
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.auth.routes import auth_bp
    from app.business.routes import business_bp
    from app.dashboard.routes import dashboard_bp
    from app.public.routes import public_bp
    from app.admin.routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(business_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)

    # Admin kontrol
    @app.context_processor
    def inject_admin():
        return dict(is_admin=lambda: current_user.is_authenticated and current_user.id == Config.ADMIN_ID)

    # CSRF token generirleýji (şablonlarda {{ csrf_token() }} işleýär)
    @app.context_processor
    def inject_csrf_token():
        return dict(csrf_token=lambda: generate_csrf())

    with app.app_context():
        db.create_all()

    return app
