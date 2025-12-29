from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    from dotenv import load_dotenv

    backend_dir = Path(__file__).parent.parent
    project_root = backend_dir.parent
    load_dotenv(backend_dir / ".env")
    load_dotenv(project_root / ".env")
except ImportError:
    pass


def login(email: str | None = None, password: str | None = None) -> str:
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_ANON_KEY")

    if not supabase_url or not supabase_key:
        raise ValueError(
            "SUPABASE_URL and SUPABASE_ANON_KEY environment variables must be set"
        )

    user_email = email or os.environ.get("SUPABASE_USER_EMAIL")
    user_password = password or os.environ.get("SUPABASE_USER_PASSWORD")

    if not user_email or not user_password:
        raise ValueError(
            "Email and password must be provided either as arguments or via "
            "SUPABASE_USER_EMAIL and SUPABASE_USER_PASSWORD environment variables"
        )

    auth_url = f"{supabase_url.rstrip('/')}/auth/v1/token?grant_type=password"
    
    data = json.dumps({"email": user_email, "password": user_password}).encode("utf-8")
    
    request = Request(
        auth_url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "apikey": supabase_key,
        },
    )

    try:
        with urlopen(request) as response:
            response_data = json.loads(response.read().decode("utf-8"))
            
            if "access_token" not in response_data:
                error_msg = response_data.get("error_description", "Login failed: No access token received")
                raise Exception(f"Login failed: {error_msg}")
            
            return response_data["access_token"]
    
    except HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            error_data = json.loads(error_body)
            error_msg = error_data.get("error_description") or error_data.get("error") or str(e)
        except (json.JSONDecodeError, AttributeError):
            error_msg = str(e)
        raise Exception(f"Login failed: {error_msg}")
    except URLError as e:
        raise Exception(f"Network error: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--email",
        type=str,
        help="User email (overrides SUPABASE_USER_EMAIL env var)",
    )
    parser.add_argument(
        "--password",
        type=str,
        help="User password (overrides SUPABASE_USER_PASSWORD env var)",
    )
    parser.add_argument(
        "--format",
        choices=["token", "header", "curl"],
        default="token",
        help="Output format: 'token' (just the token), 'header' (Authorization header), or 'curl' (curl command)",
    )

    args = parser.parse_args()

    try:
        token = login(args.email, args.password)

        if args.format == "token":
            print(token)
        elif args.format == "header":
            print(f"Authorization: Bearer {token}")
        elif args.format == "curl":
            print(f'curl -H "Authorization: Bearer {token}"')

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("\nRequired environment variables:", file=sys.stderr)
        print("  SUPABASE_URL - Your Supabase project URL", file=sys.stderr)
        print("  SUPABASE_ANON_KEY - Your Supabase anon/public key", file=sys.stderr)
        print("\nOptional environment variables (or use --email/--password):", file=sys.stderr)
        print("  SUPABASE_USER_EMAIL - User email for login", file=sys.stderr)
        print("  SUPABASE_USER_PASSWORD - User password for login", file=sys.stderr)
        print("\nNote: python-dotenv is optional. If installed, .env files will be loaded automatically.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
