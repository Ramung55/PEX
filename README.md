# PEX — Personal Expense Analyzer

A personal expense tracking website for phone and computer. This checkout currently implements only a local Django foundation and a home-page smoke test; expense features are not implemented yet.

## Local setup

Use Python **3.12** and [uv](https://docs.astral.sh/uv/getting-started/installation/). The `.python-version` file selects Python 3.12; uv can install it if it is missing. Django uses the 5.2 LTS series. The committed `uv.lock` records the exact resolved runtime and test dependencies.

From a clean checkout, open a terminal in the repository directory:

```powershell
uv sync --locked
uv run python manage.py migrate
uv run python manage.py runserver 127.0.0.1:8000
```

Open <http://127.0.0.1:8000/>. It should show “PEX — Personal Expense Analyzer” and explain that expense tracking is not implemented. Stop the server with Ctrl+C. `uv sync` also works; use `--locked` to verify the committed dependency resolution without updating it.

No PostgreSQL server, environment file, or real credential is needed for this foundation. The temporary SQLite database is created locally and ignored by Git. Issue #2 replaces this arrangement with PostgreSQL and environment settings.

These settings are **development-only**: debug mode is enabled, requests are limited to local hosts, and a fresh random development secret is generated for each process. It is not a persistent production secret and will invalidate signed data between process starts. Do not deploy this configuration; private authentication and production setup belong to later issues.

## Checks

```powershell
uv run python manage.py check
uv run pytest tests/test_home.py
uv run pytest
```

The smoke test requests the actual home route and checks its HTTP status, HTML content type, and PEX page marker. It requires neither migrations nor database access. `pytest` is configured in `pyproject.toml` through pytest-django.

## Project structure

- `manage.py`: Django command entry point.
- `pex/`: settings, URLs, home view, and WSGI/ASGI entry points.
- `templates/home.html`: minimal home page.
- `tests/test_home.py`: home-page smoke test.
- `pyproject.toml`, `uv.lock`, `.python-version`: dependencies, test configuration, and Python version.
- `_docs/`: product scope, process, and backlog references.

## Planned product

The selected stack is Django, PostgreSQL, HTMX, and Chart.js. The planned first version includes one private account with persistent login, manual KZT expense entry, customizable categories, current-month summaries, 12-month trends, automatic recurring payments, 30-day Trash, and complete-history CSV export. Hosting will use an owned server; date rules use Asia/Qyzylorda.

## Project documents and workflow

- [Project scope and decisions](_docs/plan.md)
- [Working process](_docs/process.md)
- [Backlog reference and issue links](_docs/tasks.md)
- [Project instructions](AGENTS.md)

Tasks are [GitHub issues](https://github.com/Ramung55/PEX/issues), handled one at a time. Read acceptance criteria before starting and before closing, and commit regularly. Issue #1 provides this foundation; PostgreSQL/environment configuration is #2, automated checks are #3, the responsive shell is #4, and private authentication is #5.
