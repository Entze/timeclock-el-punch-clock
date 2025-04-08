fix: fix-all-justfile fix-all-toml fix-all-python

[group('fix')]
fix-justfile PATH:
    @just fix-justfile-format {{ PATH }}

[group('fix')]
fix-all-justfile:
    @just fix-justfile justfiles/check.just
    @just fix-justfile justfiles/fix.just
    @just fix-justfile justfiles/lint.just
    @just fix-justfile justfile

[group('fix')]
fix-justfile-format PATH:
    just --unstable --fmt --justfile {{ PATH }}

[group('fix')]
fix-toml +PATHS:
    @just fix-toml-format {{ PATHS }}

[group('fix')]
fix-all-toml:
    @just fix-toml **/*.toml

[group('fix')]
fix-toml-format +PATHS:
    taplo format {{ PATHS }}

[group('fix')]
fix-python +PATHS:
    @just fix-python-format {{ PATHS }}
    @just fix-python-lint {{ PATHS }}
    @just fix-python-buildtool

[group('fix')]
fix-all-python:
    @just fix-python src/

[group('fix')]
fix-python-format +PATHS:
    ruff format {{ PATHS }}

[group('fix')]
fix-python-lint +PATHS:
    ruff check --fix {{ PATHS }}

fix-python-buildtool:
    uv lock
