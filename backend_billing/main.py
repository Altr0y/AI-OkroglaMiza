"""Entry point for the Billing Flask application."""

from __future__ import annotations

import os

from flask import Flask, jsonify
from flasgger import Swagger
from werkzeug.exceptions import BadRequest

from controllers import health_bp, card_bp
from db import init_db

BLUEPRINTS = (
    health_bp,
    card_bp,
)

SWAGGER_TEMPLATE = {
    "info": {
        "title": "AI Okrogla Miza - Billing API",
        "description": "Credit card verification and billing management API",
        "version": "1.0.0",
    },
    "basePath": "/api",
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
    app = Flask(__name__)

    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint, url_prefix="/api")

    Swagger(app, template=SWAGGER_TEMPLATE, config=SWAGGER_CONFIG)
    init_db(app)

    @app.errorhandler(BadRequest)
    def handle_bad_request(e):
        return jsonify({"error": str(e.description)}), 400

    @app.errorhandler(500)
    def handle_internal_error(e):
        return jsonify({"error": "Internal server error"}), 500

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5001"))
    app.run(host="0.0.0.0", port=port)
