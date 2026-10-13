"""Validate explicit process-environment configuration without echoing secrets."""

from django.core.exceptions import ImproperlyConfigured


def configuration(environ):
    def required(name):
        value = environ.get(name, "")
        if not value or not value.strip() or value.lower().startswith("replace_"):
            raise ImproperlyConfigured(
                f"Set {name} to a non-placeholder value; see README Local setup."
            )
        return value

    mode = environ.get("PEX_ENV", "production")
    if mode not in {"development", "production"}:
        raise ImproperlyConfigured("PEX_ENV must be development or production.")
    debug_text = environ.get("DJANGO_DEBUG", "false").lower()
    if debug_text not in {"true", "false", "1", "0"}:
        raise ImproperlyConfigured("DJANGO_DEBUG must be true/false or 1/0.")
    debug = debug_text in {"true", "1"}
    if mode == "production" and debug:
        raise ImproperlyConfigured("DJANGO_DEBUG must be false in production.")
    secret = required("DJANGO_SECRET_KEY")
    if len(secret) < 50:
        raise ImproperlyConfigured(
            "DJANGO_SECRET_KEY must contain at least 50 characters."
        )
    hosts = [host.strip() for host in required("DJANGO_ALLOWED_HOSTS").split(",")]
    if any(not host or "*" in host or "://" in host or "/" in host for host in hosts):
        raise ImproperlyConfigured(
            "DJANGO_ALLOWED_HOSTS must list explicit hostnames without wildcards or URLs."
        )
    try:
        port = int(required("DJANGO_DB_PORT"))
        if not 1 <= port <= 65535:
            raise ValueError
    except ValueError:
        raise ImproperlyConfigured(
            "DJANGO_DB_PORT must be an integer from 1 to 65535."
        ) from None
    database = {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": required("DJANGO_DB_HOST"),
        "PORT": port,
        "NAME": required("DJANGO_DB_NAME"),
        "USER": required("DJANGO_DB_USER"),
        "PASSWORD": required("DJANGO_DB_PASSWORD"),
        "OPTIONS": {"connect_timeout": 5},
    }
    return {
        "SECRET_KEY": secret,
        "DEBUG": debug,
        "ALLOWED_HOSTS": hosts,
        "DATABASES": {"default": database},
    }
