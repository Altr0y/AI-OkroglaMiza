"""Zdravstveni endpointi za vzorčno aplikacijo Flask."""

from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health_check():
    """Preprost health check za preverjanje pripravljenosti.

    ---
    tags:
      - Zdravje
    responses:
      200:
        description: Sistem deluje pravilno.
        schema:
          type: object
          properties:
            status:
              type: string
              example: ok
    """
    return jsonify(status="ok")
