import pytest
from hypothesis import settings

# Register Hypothesis profiles
settings.register_profile("ci", max_examples=100)
settings.load_profile("ci")


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()
