[group('fix')]
fix-python +PATHS:
    @just fix-python-format {{ PATHS }}
    @just fix-python-lint {{ PATHS }}

[group('fix')]
fix-all-python:
    @just fix-python src/ tests/

[group('fix')]
fix-python-format +PATHS:
    ruff format {{ PATHS }}

[group('fix')]
fix-python-lint +PATHS:
    ruff check --fix {{ PATHS }}
