from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from .routes import auth_routes, user_routes, admin_routes, campaign_routes, ad_request_routes

        app.register_blueprint(auth_routes.bp)
        app.register_blueprint(user_routes.bp)
        app.register_blueprint(admin_routes.bp)
        app.register_blueprint(campaign_routes.bp)
        app.register_blueprint(ad_request_routes.bp)

        db.create_all()

        # Import and call the seed functions
        from .seed import seed_admin, seed_data
        seed_admin()
        seed_data()

        return app
