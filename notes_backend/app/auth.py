import datetime
from typing import Dict, Any

import jwt
from flask import current_app, request
from werkzeug.exceptions import Unauthorized


# PUBLIC_INTERFACE
def create_access_token(identity: Dict[str, Any], expires_in_minutes: int = 60) -> str:
    """Create a JWT access token for the given identity dict.

    Args:
        identity: dict with at least 'id' and 'email'.
        expires_in_minutes: Token expiration time in minutes.

    Returns:
        Encoded JWT as string.
    """
    now = datetime.datetime.utcnow()
    payload = {
        "sub": str(identity.get("id")),
        "email": identity.get("email"),
        "iat": now,
        "nbf": now,
        "exp": now + datetime.timedelta(minutes=expires_in_minutes),
        "type": "access",
    }
    token = jwt.encode(payload, current_app.config["JWT_SECRET_KEY"], algorithm="HS256")
    # In PyJWT >= 2.0, encode returns str
    return token


# PUBLIC_INTERFACE
def decode_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT access token."""
    try:
        return jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
    except jwt.ExpiredSignatureError as exc:
        raise Unauthorized("Token has expired") from exc
    except jwt.InvalidTokenError as exc:
        raise Unauthorized("Invalid token") from exc


# PUBLIC_INTERFACE
def get_current_user_id_from_request() -> int:
    """Extract and validate the Bearer token from the Authorization header and return user id."""
    auth_header = request.headers.get("Authorization", "")
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise Unauthorized("Missing or invalid Authorization header")
    payload = decode_token(parts[1])
    try:
        return int(payload["sub"])
    except (KeyError, ValueError) as exc:
        raise Unauthorized("Invalid token payload") from exc
