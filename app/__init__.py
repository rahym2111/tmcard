import os
from flask import Flask
from flask_login import current_user
from flask_wtf.csrf import generate_csrf
from app.config import Config
from app.extensions import db, login_manager, csrf

def create_app():
    # instance_relative_config parametrini aýyrdyk!
    app = Flask(__name__)
    app.config.from_object(Config)

    # Database we Upload papkalarynyň varlygyny üpjün etmek
    for folder in [Config.UPLOAD_FOLDER, Config.LOGO_FOLDER, Config.COVER_FOLDER, Config.PRODUCT_FOLDER]:
        os.makedirs(folder, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
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

    @app.context_processor
    def inject_admin():
        return dict(is_admin=lambda: current_user.is_authenticated and current_user.id == Config.ADMIN_ID)

    @app.context_processor
    def inject_csrf_token():
        return dict(csrf_token=lambda: generate_csrf())

    with app.app_context():
        db.create_all()

    return app
