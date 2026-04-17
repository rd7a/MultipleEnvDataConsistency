# Framework Rules

## Configuration
- All environment config (base URLs, thresholds) must live in `config/environments.yaml`.
- Never hardcode base URLs, timeouts, or thresholds anywhere in test or source code.
- Adding a new environment means adding a new block to `environments.yaml` only — no code changes required.

## Test Isolation
- Test files must not import from other test files.
- Each test must be independently runnable without relying on state from a previous test.
- Session-scoped fixtures are allowed for shared I/O (HTTP calls, YAML reads) but must not carry mutable state.

## Directory Layout
- `config/`     — YAML environment definitions only
- `src/validators/` — schema and field validators only
- `test_data/`  — JSON input files for parametrized tests only
- `tests/`      — pytest test files only
- `.claude/rules/` — Claude coding rules
- `.claude/skills/` — Claude skill prompts
- `reports/`    — generated outputs (gitignored)

## CLI Flag
- The `--env` flag is the single mechanism for environment selection.
- `pytest_addoption` and `pytest_collection_modifyitems` in the top-level `conftest.py` are the only places that reference `--env`.

## CI
- The CI pipeline must install dependencies from `pyproject.toml [dev]` — no ad-hoc `pip install` steps for project packages.
- Allure CLI is installed separately in CI (it is not a Python package).
- Pipeline must fail on any test failure — never use `|| true` or `continue-on-error` on test steps.
