lint: lint-all-python

[group('lint')]
lint-python +PATHS:
    @just lint-python-analysis {{ PATHS }}
    @just lint-python-typecheck {{ PATHS }}

[group('lint')]
lint-all-python:
    @just lint-python src/

[group('lint')]
lint-python-analysis +PATHS:
    ruff check {{ PATHS }}

[group('lint')]
lint-python-typecheck +PATHS:
    mypy {{ PATHS }}
    pyright {{ PATHS }}
