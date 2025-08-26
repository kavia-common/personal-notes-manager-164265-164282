"""ASGI/WSGI entrypoint for the Notes Backend.

This module exposes a module-level `app` variable so process managers and ASGI/WSGI servers
(e.g., gunicorn, uvicorn) can import `main:app`.

It uses the application factory from app.create_app to initialize the Flask application.
"""

import os

from app import create_app

# PUBLIC_INTERFACE
def get_app():
    """Return the Flask app instance created via the application factory.

    Returns:
        Flask: The configured Flask application.
    """
    return create_app()


# Expose the app at module level for ASGI/WSGI servers expecting `module:app`
app = get_app()


if __name__ == "__main__":
    # Allow running directly (useful for quick local tests)
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "3001"))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host=host, port=port, debug=debug)
