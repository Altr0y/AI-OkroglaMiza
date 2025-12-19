from flask import Blueprint, jsonify, g

from middleware import supabase_auth_middleware

user_bp = Blueprint("user", __name__)


@user_bp.get("/user/me")
@supabase_auth_middleware
def get_current_user():
    """Get Current User

    ---
    tags:
      - User
    security:
      - Bearer: []
    responses:
      200:
        description: Current user information
        schema:
          type: object
          properties:
            id:
              type: string
              example: "123e4567-e89b-12d3-a456-426614174000"
            email:
              type: string
              example: "user@example.com"
      401:
        description: Unauthorized - Invalid or missing token
    """
    return jsonify(
        id=g.user["id"],
        email=g.user["email"],
    )

