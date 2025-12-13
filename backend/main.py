"""Vstopna točka za vzorčno Flask aplikacijo."""

from __future__ import annotations

import os

from flask import Flask
from flasgger import Swagger

from controllers import health_bp

BLUEPRINTS = (
    health_bp,
)

SWAGGER_TEMPLATE = {
    "info": {
        "title": "AI Okrogla Miza API",
        "description": "Samodejno generirana dokumentacija za backend.",
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
    """Lokalni zagon in gunicorn."""
    app = Flask(__name__)
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint, url_prefix="/api")
    Swagger(app, template=SWAGGER_TEMPLATE, config=SWAGGER_CONFIG)
    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
