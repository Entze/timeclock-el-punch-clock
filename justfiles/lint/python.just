[group('lint')]
lint-python +PATHS:
    @just lint-python-lint {{ PATHS }}
    @just lint-python-typecheck {{ PATHS }}

[group('lint')]
lint-all-python:
    @just lint-python src/
    @just lint-python-lint tests/

[group('lint')]
lint-python-lint +PATHS:
    ruff check {{ PATHS }}

[group('lint')]
lint-python-typecheck +PATHS:
    mypy {{ PATHS }}
    pyright {{ PATHS }}
