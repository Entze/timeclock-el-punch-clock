[group('check')]
check-toml +PATHS:
    @just check-toml-format {{ PATHS }}

[group('check')]
check-all-toml:
    @just check-toml **/*.toml

[group('check')]
check-toml-format +PATHS:
    taplo format --check {{ PATHS }}
