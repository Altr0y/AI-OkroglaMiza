"""Here you need to add all controllers so they are visible in main"""

from .health import health_bp
from .user import user_bp

__all__ = [
    "health_bp",
    "user_bp",
]
