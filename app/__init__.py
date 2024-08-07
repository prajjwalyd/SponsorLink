from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_jwt_extended import JWTManager
from flask_restful import Api

db = SQLAlchemy()
login_manager = LoginManager()

def SponsorLink():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    jwt = JWTManager(app)
    api = Api(app)

    with app.app_context():
        from .routes import auth_routes, user_routes, admin_routes, campaign_routes, ad_request_routes
        from .api import api_bp, register_resources

        app.register_blueprint(auth_routes.bp)
        app.register_blueprint(user_routes.bp)
        app.register_blueprint(admin_routes.bp)
        app.register_blueprint(campaign_routes.bp)
        app.register_blueprint(ad_request_routes.bp)
        app.register_blueprint(api_bp)

        # Seed the database
        from .seed import seed_admin, seed_data
        db.create_all()
        seed_admin()
        seed_data()
        register_resources(api) # Register API resources

    return app
