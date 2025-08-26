from flask import Flask
from flask_cors import CORS
from flask_smorest import Api

from .config import get_config
from .models import db
from .routes.health import blp as health_blp
from .routes.auth import blp as auth_blp
from .routes.notes import blp as notes_blp


# PUBLIC_INTERFACE
def create_app() -> Flask:
    """Application factory that configures Flask, SQLAlchemy, CORS, and API docs."""
    app = Flask(__name__)
    cfg = get_config()

    # Core config
    app.config["SECRET_KEY"] = cfg.SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = cfg.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = cfg.SQLALCHEMY_TRACK_MODIFICATIONS

    # API docs configuration
    app.url_map.strict_slashes = False
    app.config["API_TITLE"] = cfg.API_TITLE
    app.config["API_VERSION"] = cfg.API_VERSION
    app.config["OPENAPI_VERSION"] = cfg.OPENAPI_VERSION
    app.config["OPENAPI_URL_PREFIX"] = cfg.OPENAPI_URL_PREFIX
    app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Initialize extensions
    CORS(app, resources={r"/*": {"origins": cfg.CORS_ORIGINS}})
    db.init_app(app)

    # Create tables if they do not exist (simple setup)
    with app.app_context():
        db.create_all()

    # API and blueprints
    api = Api(app)
    api.register_blueprint(health_blp)
    api.register_blueprint(auth_blp)
    api.register_blueprint(notes_blp)

    return app


# Keep a default app instance for compatibility with run.py
app = create_app()
