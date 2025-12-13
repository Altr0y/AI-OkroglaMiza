"""Paket controllerjev, ki izpostavi vse blueprinte."""

from .health import health_bp

__all__ = [
    "health_bp",
]
