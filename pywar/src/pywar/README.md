
This document is supposed to cover only local `src/` information. For whole scope, please go to 
[the main README file](../../README.md).

# Usage:

# Installation:

For a production case, install the .whl package using `pip`.

For a development, setup a pyenv, and install environment using `uv sync --active`.

### Running:
Run (in pyenv venv) `python -m pywar`. It will execute `__main__.py`.

# Building:
Use `uv build`.

# Technical information:

# Features:
- UV build system with package build
- Main executable module
- Django ORM for Sqlite3 database access
- Static analysis

### Technical TODO items in context of deployment-readiness:
- Enforce static analysis quality gates
  - No warnings and errors from static checkers: mypy, Ruff, isort
  - Check code coverage results, quality gate for unit >70%.
  - TBD quality gate for integration / E2E testing.
- Logging facility
- Database file location - system should read and provide an equivalent of AppData for SQLite db.
- Database cleanup functionality
- Unit tests for the game logic
- Integration tests for database access services
- Transactions - commit changes once and give control to service user.

### My wishlist:
- Play more with database joins using Django ORM.
- Check ability to use different database back-ends and replace them in `GameHistoryService`.
- Main menu?
