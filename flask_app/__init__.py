from flask import Flask
from flask_session import Session
from .config import config


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Importing and register blueprints
    from .controllers.auth_controller import auth_bp
    from .controllers.client_controller import client_bp
    from .controllers.policy_controller import policy_bp
    from .controllers.claim_controller import claim_bp
    from .controllers.stats_controller import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(policy_bp)
    app.register_blueprint(claim_bp)
    app.register_blueprint(dashboard_bp)

    # Configuring session management
    Session(app)

    # Set caching headers for all responses
    # off because of back buttons doesnt work on Safari
    @app.after_request
    def add_header(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    return app
