check: check-all-justfile check-all-toml check-all-yaml check-python-buildtool check-all-python

[group('check')]
check-justfile +PATHS:
    @just check-justfile-format {{ PATHS }}

[group('check')]
check-all-justfile:
    @just check-justfile justfile justfiles/*.just

[group('check')]
check-justfile-format +PATHS:
    #!/usr/bin/env sh
    for path in {{ PATHS }}; do
        just --unstable --fmt --check --justfile $path
    done

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

[group('check')]
check-yaml +PATHS:
    @just check-yaml-format {{ PATHS }}

[group('check')]
check-all-yaml:
    @just check-yaml .yamllint *.yml

[group('check')]
check-yaml-format +PATHS:
    yamllint {{ PATHS }}

[group('check')]
check-python +PATHS:
    @just check-python-format {{ PATHS }}

[group('check')]
check-all-python:
    @just check-python src/

[group('check')]
check-python-format +PATHS:
    ruff format --check {{ PATHS }}
