import os
from dataclasses import dataclass


@dataclass
class Config:
    """Base configuration loaded from environment variables."""
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me")
    # Database connection string. Expected from dependency notes_database
    # e.g., postgresql+psycopg2://user:pass@host:port/dbname
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL", "sqlite:///notes.db")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    API_TITLE: str = os.getenv("API_TITLE", "Notes API")
    API_VERSION: str = os.getenv("API_VERSION", "v1")
    OPENAPI_VERSION: str = os.getenv("OPENAPI_VERSION", "3.0.3")
    OPENAPI_URL_PREFIX: str = os.getenv("OPENAPI_URL_PREFIX", "/docs")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "change-me-too")
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")


def get_config() -> Config:
    """
    PUBLIC_INTERFACE
    Returns the populated configuration object.

    This function reads environment variables and returns a strongly typed
    config object used by the Flask app to initialize services.
    """
    return Config()
