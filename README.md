# PEX — Personal Expense Analyzer

A personal expense tracking website for phone and computer. This checkout implements a Django foundation, environment-based PostgreSQL settings, and tests. Expense features are not implemented yet.

## Local setup

Use Python **3.12**, [uv](https://docs.astral.sh/uv/getting-started/installation/), and Docker with the official PostgreSQL **17** image (or a supported existing PostgreSQL installation). `.python-version` selects Python 3.12 and `uv.lock` records exact dependencies. Docker is only a local setup convenience, not the chosen production hosting arrangement.

From a clean checkout, open PowerShell in the repository directory:

```powershell
uv sync --locked
Copy-Item .env.example .env
```

Edit `.env`: replace both `REPLACE_...` values with independently generated random strings. Generate each with `uv run python -c "import secrets; print(secrets.token_hex(32))"`. The secret must be at least 50 characters. These are disposable local credentials, not existing production credentials. `.env` is ignored by Git; never commit it.

Export that file explicitly into the current terminal (literal KEY=value lines only, no shell evaluation):

```powershell
Get-Content .env | ForEach-Object {
    if ($_ -match '^([A-Z][A-Z0-9_]*)=(.*)$') {
        [Environment]::SetEnvironmentVariable($Matches[1], $Matches[2], 'Process')
    }
}
```

Django intentionally does **not** auto-load `.env`. This prevents a production process from silently inheriting a development file. Start the application from the same terminal after exporting values.

For a fresh disposable database, use this explicitly named container, published only on localhost. Before starting, verify that neither the name nor port is already in use; choose another name/port and update `.env` if necessary.

```powershell
$env:POSTGRES_PASSWORD = $env:DJANGO_DB_PASSWORD
docker run --name pex-local-postgres --detach `
    --publish 127.0.0.1:55432:5432 `
    --env POSTGRES_PASSWORD `
    --env POSTGRES_USER=pex_local `
    --env POSTGRES_DB=pex_local postgres:17
Remove-Item Env:POSTGRES_PASSWORD
docker exec pex-local-postgres pg_isready -U pex_local -d pex_local
```

Repeat the readiness check until it accepts connections, then:

```powershell
uv run python manage.py migrate
uv run python manage.py check
uv run python manage.py runserver 127.0.0.1:8000
```

Open <http://127.0.0.1:8000/> and verify the PEX development heading. Stop the server with Ctrl+C. No expense models or private login are provided yet. Reuse the local database with `docker stop pex-local-postgres` and `docker start pex-local-postgres`; the same container retains its data. This disposable example does not add a named or host volume.

The image initializes `pex_local` as a local superuser, so it can create Django's isolated `test_pex_local` test database. Use this only for the disposable local example. For an existing PostgreSQL installation, use a dedicated application role that owns the chosen database and has `CREATEDB` for tests; it need not be a superuser. Never point tests at production. Separate restricted production permissions belong to deployment preparation (#30).

To permanently remove **only this disposable example**, first check its name and port with `docker ps -a --filter name=pex-local-postgres`, then run `docker rm --force --volumes pex-local-postgres`. Do not use a broad prune, remove another project's container, or delete a shared database. If using an existing installation, remove only the explicitly created disposable database/role through its administrator's normal tools after confirming their identities.

## Environment contract

| Variable | Meaning |
|---|---|
| `PEX_ENV` | `development` or `production`; defaults to production |
| `DJANGO_DEBUG` | `true`/`false` or `1`/`0`; defaults false; true is rejected in production |
| `DJANGO_SECRET_KEY` | Required non-placeholder random value, at least 50 characters |
| `DJANGO_ALLOWED_HOSTS` | Required comma-separated explicit hostnames, no wildcard or URL |
| `DJANGO_DB_HOST` | Required PostgreSQL hostname/address |
| `DJANGO_DB_PORT` | Required integer 1–65535 |
| `DJANGO_DB_NAME` | Required database name |
| `DJANGO_DB_USER` | Required database role |
| `DJANGO_DB_PASSWORD` | Required non-placeholder password |

Missing or invalid settings fail with the variable name and setup guidance, without echoing supplied secrets. PostgreSQL is mandatory for application and tests; there is no SQLite fallback. Production mode supplies no development key, credentials, or host defaults. This is configuration preparation, not a production deployment configuration: HTTPS, secure cookie policy, infrastructure, and restricted server roles remain #30.

`TIME_ZONE=Asia/Qyzylorda` and `USE_TZ=True`; application-local dates use Qyzylorda even if the host uses another timezone. At 19:00 UTC, the local calendar date advances to the next day.

## Checks

With the environment exported and the disposable PostgreSQL database ready:

```powershell
uv run python manage.py check
uv run pytest tests/test_home.py
uv run pytest
```

The suite validates configuration errors/production defaults, the local midnight boundary, and an actual PostgreSQL test-database connection, in addition to the home-page HTTP smoke test. Django/pytest creates and removes the isolated test database; application migrations use the configured application database.

### Automated checks

After exporting the local environment, run the same non-mutating checks used by CI:

```powershell
uv run --locked ruff format --check .
uv run --locked ruff check .
uv run --locked python manage.py check
uv run --locked python manage.py migrate --noinput
uv run --locked pytest tests/test_home.py
uv run --locked pytest
```

The format check reports required changes without editing source. To intentionally apply formatting, run `uv run ruff format .`; review the resulting diff. Ruff linting selects basic errors and import ordering, targets Python 3.12, and excludes generated environments/build directories. Ruff's exact version is recorded in `uv.lock`.

`.github/workflows/checks.yml` runs on pushes and pull requests using Python 3.12, uv 0.13.0, locked dependency installation, and separately named format/lint/Django/migration/smoke/full-suite steps. It provisions its own PostgreSQL 17 service with readiness health checks and disposable test-only values; no user credentials or repository secrets are required. Any failed step fails the job; an unavailable database cannot produce a successful test result. The workflow does not deploy the application.

Verification includes a passing run and temporary intentional format/lint/test failures on disposable review branches, followed by clean passing results. Run links and final evidence are recorded on issue #3; intentional defects must not remain in the implementation branch.

## Project structure and planned scope

- `manage.py`: Django command entry point.
- `pex/`: validated settings, URLs, home view, and WSGI/ASGI entry points.
- `templates/home.html`: minimal page.
- `tests/`: home and settings/PostgreSQL checks.
- `pyproject.toml`, `uv.lock`, `.python-version`: dependency and test configuration.
- `.env.example`: placeholder-only environment template.
- `_docs/`: product scope, process, and backlog references.

The selected stack is Django, PostgreSQL, HTMX, and Chart.js. The planned private application tracks KZT spending, categories, recurring payments, reports, 30-day Trash, and CSV export; hosting is an owned server to be selected later.

## Project documents and workflow

- [Project scope and decisions](_docs/plan.md)
- [Working process](_docs/process.md)
- [Backlog reference and issue links](_docs/tasks.md)
- [Project instructions](AGENTS.md)

Tasks are [GitHub issues](https://github.com/Ramung55/PEX/issues), handled one at a time. Issue #1 provides the foundation; #2 supplies PostgreSQL/environment settings; #3 supplies automated checks; #4 supplies the responsive shell; #5 supplies private authentication. Read acceptance criteria, commit regularly, and follow the engineer instructions when recording implementation.
