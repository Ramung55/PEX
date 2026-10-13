import os
import subprocess
import sys
from datetime import datetime
from datetime import timezone as datetime_timezone

import pytest
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import connection
from django.utils import timezone

from pex.environment import configuration


@pytest.fixture
def environment():
    return {
        "PEX_ENV": "development",
        "DJANGO_DEBUG": "true",
        "DJANGO_SECRET_KEY": "test-only-" * 8,
        "DJANGO_ALLOWED_HOSTS": "localhost,127.0.0.1",
        "DJANGO_DB_HOST": "127.0.0.1",
        "DJANGO_DB_PORT": "55432",
        "DJANGO_DB_NAME": "pex_test_config",
        "DJANGO_DB_USER": "pex_test_role",
        "DJANGO_DB_PASSWORD": "test-only-password",
    }


def test_explicit_configuration(environment):
    result = configuration(environment)
    assert result["DEBUG"] is True
    assert result["ALLOWED_HOSTS"] == ["localhost", "127.0.0.1"]
    db = result["DATABASES"]["default"]
    assert db["ENGINE"] == "django.db.backends.postgresql"
    assert db["PORT"] == 55432
    assert db["NAME"] == environment["DJANGO_DB_NAME"]
    assert db["PASSWORD"] == environment["DJANGO_DB_PASSWORD"]


@pytest.mark.parametrize(
    "name",
    [
        "DJANGO_SECRET_KEY",
        "DJANGO_ALLOWED_HOSTS",
        "DJANGO_DB_HOST",
        "DJANGO_DB_PORT",
        "DJANGO_DB_NAME",
        "DJANGO_DB_USER",
        "DJANGO_DB_PASSWORD",
    ],
)
def test_required_environment_has_no_fallback(environment, name):
    del environment[name]
    with pytest.raises(ImproperlyConfigured, match=name):
        configuration(environment)


@pytest.mark.parametrize("value", ["0", "65536", "not-a-port-sensitive-marker"])
def test_invalid_port_is_safe(environment, value):
    environment["DJANGO_DB_PORT"] = value
    with pytest.raises(ImproperlyConfigured) as error:
        configuration(environment)
    assert "DJANGO_DB_PORT" in str(error.value)
    assert value not in str(error.value)
    assert environment["DJANGO_DB_PASSWORD"] not in str(error.value)


@pytest.mark.parametrize(
    "name,value",
    [
        ("PEX_ENV", "unknown"),
        ("DJANGO_DEBUG", "yes"),
        ("DJANGO_ALLOWED_HOSTS", "*"),
        ("DJANGO_ALLOWED_HOSTS", "https://example.com"),
        ("DJANGO_ALLOWED_HOSTS", "localhost,,example.com"),
        ("DJANGO_SECRET_KEY", "short"),
        ("DJANGO_DB_PASSWORD", "REPLACE_WITH_PASSWORD"),
    ],
)
def test_unsafe_configuration_rejected(environment, name, value):
    environment[name] = value
    with pytest.raises(ImproperlyConfigured):
        configuration(environment)


def test_production_is_default_and_rejects_debug(environment):
    del environment["PEX_ENV"]
    with pytest.raises(ImproperlyConfigured, match="DJANGO_DEBUG"):
        configuration(environment)
    environment["DJANGO_DEBUG"] = "false"
    assert configuration(environment)["DEBUG"] is False


def test_production_has_no_development_secret(environment):
    environment["PEX_ENV"] = "production"
    environment["DJANGO_DEBUG"] = "false"
    del environment["DJANGO_SECRET_KEY"]
    with pytest.raises(ImproperlyConfigured, match="DJANGO_SECRET_KEY"):
        configuration(environment)


def test_management_command_reports_missing_password_safely():
    invalid_environment = dict(os.environ)
    invalid_environment.pop("DJANGO_DB_PASSWORD", None)
    result = subprocess.run(
        [sys.executable, str(settings.BASE_DIR / "manage.py"), "check"],
        env=invalid_environment,
        capture_output=True,
        text=True,
        timeout=15,
    )
    output = result.stdout + result.stderr
    assert result.returncode != 0
    assert "Set DJANGO_DB_PASSWORD" in output
    assert os.environ["DJANGO_DB_PASSWORD"] not in output
    assert os.environ["DJANGO_SECRET_KEY"] not in output


@pytest.mark.parametrize(
    "instant,expected",
    [
        (datetime(2026, 10, 12, 18, 59, tzinfo=datetime_timezone.utc), "2026-10-12"),
        (datetime(2026, 10, 12, 19, 0, tzinfo=datetime_timezone.utc), "2026-10-13"),
    ],
)
def test_qyzylorda_midnight(instant, expected):
    assert settings.TIME_ZONE == "Asia/Qyzylorda"
    assert settings.USE_TZ is True
    assert timezone.localdate(instant).isoformat() == expected


@pytest.mark.django_db
def test_actual_test_database_is_postgresql():
    assert connection.vendor == "postgresql"
    with connection.cursor() as cursor:
        cursor.execute("SELECT current_database(), version()")
        name, version = cursor.fetchone()
    assert name.startswith("test_")
    assert "PostgreSQL" in version
