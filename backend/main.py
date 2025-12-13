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
        "description": "Samodejno generirana dokumentacija za vzorčno aplikacijo.",
        "version": "1.0.0",
    },
    "basePath": "/api",
}


def create_app() -> Flask:
    """Tovarniška funkcija aplikacije za lokalni zagon in gunicorn."""
    app = Flask(__name__)
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint, url_prefix="/api")
    Swagger(app, template=SWAGGER_TEMPLATE)
    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
