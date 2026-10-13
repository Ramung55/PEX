# Working Process

## Task tracking

Tasks are [GitHub issues in Ramung55/PEX](https://github.com/Ramung55/PEX/issues). Work on one issue at a time; use the issue as the source for current task status, discussion, and acceptance criteria.

`_docs/tasks.md` retains the original handoff descriptions and issue links. It is a local reference, not a separate status tracker. `_docs/plan.md` records agreed scope and product behavior.

## Before starting

- Read the issue's goal, description, and acceptance criteria.
- Read the applicable project instructions in `AGENTS.md` and relevant sections of `_docs/plan.md`.
- If the issue has no explicit acceptance criteria, define clear completion checks from its description before implementation.
- Identify prerequisites and unresolved decisions before starting dependent work.
- Ask before adding dependencies to `pyproject.toml`.

## While working

- Keep changes focused on the selected issue.
- Commit regularly, using messages that explain the change and refer to the issue when applicable.
- Update relevant documents when requirements or implementation decisions change.

## Before closing

- Read the acceptance criteria again and verify each one.
- Run the checks appropriate to the change and record the results in the issue.
- Commit the completed work and ensure relevant documents reflect the result.
- Close the issue only when its acceptance criteria are satisfied; otherwise record what remains.

## Project commands

After the initial project setup provides the configuration and tests:

- `uv sync` — install dependencies.
- `uv run pytest` — run the whole suite.
- `uv run pytest tests/test_home.py` — run the home-page test file.
