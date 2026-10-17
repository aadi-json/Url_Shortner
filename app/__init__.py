import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_object="config.Config"):
    # Use a writable instance directory on Vercel
    if os.environ.get("VERCEL"):
        instance_path = "/tmp/shortly_instance"
    else:
        instance_path = None

    app = Flask(
        __name__,
        instance_path=instance_path,
    )

    # Load application configuration
    app.config.from_object(config_object)

    # Configure writable storage on Vercel
    if os.environ.get("VERCEL"):
        os.makedirs(app.instance_path, exist_ok=True)

        # Temporary SQLite database
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            "sqlite:////tmp/shortly.db"
        )

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Configure Flask-Login
    login_manager.login_view = "auth.login"

    # Import models
    from app import models

    # Register blueprints
    from app.auth import bp as auth_bp
    from app.main import bp as main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # Create missing database tables on Vercel
    if os.environ.get("VERCEL"):
        with app.app_context():
            db.create_all()

            # Print tables in Vercel runtime logs for verification
            from sqlalchemy import inspect
            print("Database tables:", inspect(db.engine).get_table_names())

    return app