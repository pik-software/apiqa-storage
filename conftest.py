import os
import django


def pytest_configure():
    os.environ.setdefault("ENVIRONMENT", "test")
    os.environ.setdefault("DATABASE_URL",
                          "postgres://postgres:postgres@127.0.0.1:5432"
                          "/apiqa-storage")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_project.settings")

    django.setup()
