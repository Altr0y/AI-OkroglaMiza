"""Entry point for the Flask application."""

from __future__ import annotations

import os

from flask import Flask, jsonify
from flasgger import Swagger
from werkzeug.exceptions import Unauthorized

from controllers import health_bp, user_bp
from db import init_db

BLUEPRINTS = (
    health_bp,
    user_bp,
)

SWAGGER_TEMPLATE = {
    "info": {
        "title": "AI Okrogla Miza API",
        "description": "Automatically generated documentation for the backend.",
        "version": "1.0.0",
    },
    "basePath": "/api",
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter your Supabase JWT token in the format: Bearer <token>",
        }
    },
}

SWAGGER_CONFIG = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        },
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
}


def create_app() -> Flask:
    """Local run and gunicorn."""
    app = Flask(__name__)
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint, url_prefix="/api")
    Swagger(app, template=SWAGGER_TEMPLATE, config=SWAGGER_CONFIG)
    init_db(app)

    # Error handler for authentication errors
    @app.errorhandler(Unauthorized)
    def handle_unauthorized(e):
        return jsonify({"error": str(e.description)}), 401

    return app


app = create_app()


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)