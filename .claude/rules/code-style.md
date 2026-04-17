# Code Style

## Type Hints
- All functions must use type hints on parameters and return types.
- Use built-in generics (`list[str]`, `dict[str, Any]`) — not `List`, `Dict` from `typing`.

## Validators
- All validation logic must live in `src/validators/`.
- Validator functions must return data (missing fields, out-of-range values) — never raise exceptions or call `assert` internally.
- Tests call validators and assert on their output.

## Imports
- Standard library imports first, then third-party, then local — separated by blank lines.
- Never use wildcard imports (`from module import *`).

## Comments
- Only add a comment when the WHY is non-obvious.
- Do not comment what the code does — well-named identifiers do that.
- Section dividers (e.g. `# ---`) are allowed in conftest.py and long config files.

## Constants
- Module-level constants use UPPER_SNAKE_CASE.
- No magic numbers or strings inline — define as constants at module top.

## File Length
- Keep test files under 150 lines. Split into multiple files if exceeded.
- Validator files should contain one logical group of validators per file.
