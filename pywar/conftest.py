import os
from typing import Any
from django.conf import settings
import pytest


MY_HOME = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(MY_HOME, "pywar.sqlite3")


# I really hate doing this:
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


def pytest_configure():
    # settings.configure(DATABASES=...)
    settings.configure(
        DEBUG=False,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": DB_PATH,
                "USER": "",
                "PASSWORD": "",
                "HOST": "",
                "PORT": "",
            }
        },
        INSTALLED_APPS=("pywar.db",),
    )


@pytest.fixture(autouse=True)
def use_dummy_cache_backend(settings: Any) -> None:
    settings.CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }
