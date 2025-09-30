"""Fixtures specific to API integration tests"""
import pytest


@pytest.fixture(autouse=True)
def auto_clean_database(clean_database):
    """Automatically use clean_database for all tests in this directory"""
    return clean_database


@pytest.fixture(autouse=True)
def auto_override_database_url(override_database_url):
    """Automatically override database URL for all tests in this directory"""
    return override_database_url
