import os

import pytest
import django


def pytest_configure():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_project.settings")
    django.setup()


@pytest.fixture(scope='session')
def base_url(live_server):
    return live_server.url


@pytest.fixture(scope='function', autouse=True)
def _skip_sensitive(request):
    """Pytest-selenium patch: don't Skip destructive tests"""
