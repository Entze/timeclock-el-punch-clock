[group('check')]
check-python +PATHS:
    @just check-python-format {{ PATHS }}

[group('check')]
check-all-python:
    @just check-python src/ tests/

[group('check')]
check-python-format +PATHS:
    ruff format --check {{ PATHS }}
