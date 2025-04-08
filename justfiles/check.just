check: check-all-toml check-all-python

[group('check')]
check-python +PATHS:
    @just check-python-format {{ PATHS }}
    @just check-python-buildtool

[group('check')]
check-all-python:
    @just check-python src/

[group('check')]
check-python-format +PATHS:
    ruff format --check {{ PATHS }}

[group('check')]
check-python-buildtool:
    uv lock --check

[group('check')]
check-toml +PATHS:
    @just check-toml-format {{ PATHS }}

[group('check')]
check-all-toml:
    @just check-toml **/*.toml

[group('check')]
check-toml-format +PATHS:
    taplo format --check {{ PATHS }}
