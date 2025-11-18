"""Minimal unit tests for py_ocpi.core.config Settings"""
import pytest
from unittest.mock import patch
from py_ocpi.core.config import Settings


class TestSettings:
    """Test Settings class and validators"""

    def test_default_settings(self):
        """Test default settings values"""
        settings = Settings()
        assert settings.ENVIRONMENT == "production"
        assert settings.NO_AUTH is False
        assert settings.PROJECT_NAME == "OCPI"
        assert settings.COUNTRY_CODE == "US"
        assert settings.PARTY_ID == "NON"
        assert settings.PROTOCOL == "https"
        assert settings.TRAILING_SLASH is True
        assert settings.CI_STRING_LOWERCASE_PREFERENCE is True

    def test_cors_origins_from_string(self):
        """Test CORS origins parsed from comma-separated string"""
        settings = Settings(BACKEND_CORS_ORIGINS="http://localhost,http://example.com")
        assert len(settings.BACKEND_CORS_ORIGINS) == 2
        assert str(settings.BACKEND_CORS_ORIGINS[0]) == "http://localhost/"
        assert str(settings.BACKEND_CORS_ORIGINS[1]) == "http://example.com/"

    def test_cors_origins_from_list(self):
        """Test CORS origins from list"""
        origins = ["http://localhost", "http://example.com"]
        settings = Settings(BACKEND_CORS_ORIGINS=origins)
        assert len(settings.BACKEND_CORS_ORIGINS) == 2
        assert str(settings.BACKEND_CORS_ORIGINS[0]) == "http://localhost/"
        assert str(settings.BACKEND_CORS_ORIGINS[1]) == "http://example.com/"

    def test_cors_origins_empty_list(self):
        """Test default empty CORS origins list"""
        settings = Settings()
        assert settings.BACKEND_CORS_ORIGINS == []

    def test_custom_values(self):
        """Test custom configuration values"""
        settings = Settings(
            ENVIRONMENT="development",
            NO_AUTH=True,
            COUNTRY_CODE="DE",
            PARTY_ID="ABC",
            CI_STRING_LOWERCASE_PREFERENCE=False,
        )
        assert settings.ENVIRONMENT == "development"
        assert settings.NO_AUTH is True
        assert settings.COUNTRY_CODE == "DE"
        assert settings.PARTY_ID == "ABC"
        assert settings.CI_STRING_LOWERCASE_PREFERENCE is False
