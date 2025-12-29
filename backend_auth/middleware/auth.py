"""Supabase authentication middleware"""

from __future__ import annotations

import json
import os
from functools import wraps
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from flask import g, request
from werkzeug.exceptions import Unauthorized


def verify_supabase_token(token: str) -> dict:
    """Verify a Supabase JWT token and return user information."""
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_ANON_KEY")

    if not supabase_url or not supabase_key:
        raise ValueError(
            "SUPABASE_URL and SUPABASE_ANON_KEY environment variables must be set"
        )

    # Use Supabase's user endpoint to verify the token
    user_url = f"{supabase_url.rstrip('/')}/auth/v1/user"
    
    request_obj = Request(
        user_url,
        headers={
            "Authorization": f"Bearer {token}",
            "apikey": supabase_key,
        },
    )

    try:
        with urlopen(request_obj) as response:
            response_data = json.loads(response.read().decode("utf-8"))
            
            if "id" not in response_data:
                raise Unauthorized("Invalid or expired token")
            
            return {
                "id": response_data.get("id"),
                "email": response_data.get("email"),
                "user_metadata": response_data.get("user_metadata", {}),
                "app_metadata": response_data.get("app_metadata", {}),
            }
    
    except HTTPError as e:
        if e.code == 401:
            raise Unauthorized("Invalid or expired token")
        error_body = e.read().decode("utf-8")
        try:
            error_data = json.loads(error_body)
            error_msg = error_data.get("error_description") or error_data.get("error") or str(e)
        except (json.JSONDecodeError, AttributeError):
            error_msg = str(e)
        raise Unauthorized(f"Authentication failed: {error_msg}")
    except URLError as e:
        raise Unauthorized(f"Network error: {e}")


def supabase_auth_middleware(f):
    """Middleware decorator to authenticate requests using Supabase.

    Usage:
        @app.route('/protected')
        @supabase_auth_middleware
        def protected_route():
            user_id = g.user['id']
            return jsonify(user=g.user)
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise Unauthorized("Authorization header is missing")

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise Unauthorized("Invalid Authorization header format. Expected: Bearer <token>")

        token = parts[1]

        try:
            user_data = verify_supabase_token(token)
            g.user = user_data
            g.token = token

        except Unauthorized:
            raise
        except Exception as e:
            raise Unauthorized(f"Authentication failed: {str(e)}")

        return f(*args, **kwargs)

    return decorated_function


def optional_supabase_auth_middleware(f):
    """Optional authentication middleware that doesn't raise errors if no token is provided.
    If a token is provided, it will be verified and the user information will be stored in the g object.

    Usage:
        @app.route('/optional-protected')
        @optional_supabase_auth_middleware
        def optional_protected_route():
            if hasattr(g, 'user'):
                return jsonify(user=g.user, authenticated=True)
            return jsonify(authenticated=False)
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                token = parts[1]
                try:
                    user_data = verify_supabase_token(token)
                    g.user = user_data
                    g.token = token
                except Exception:
                    pass

        return f(*args, **kwargs)

    return decorated_function
