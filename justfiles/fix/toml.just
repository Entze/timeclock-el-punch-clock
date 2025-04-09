[group('fix')]
fix-toml +PATHS:
    @just fix-toml-format {{ PATHS }}

[group('fix')]
fix-all-toml:
    @just fix-toml **/*.toml

[group('fix')]
fix-toml-format +PATHS:
    taplo format {{ PATHS }}
