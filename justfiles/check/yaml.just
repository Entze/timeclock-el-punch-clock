[group('check')]
check-yaml +PATHS:
    @just check-yaml-format {{ PATHS }}

[group('check')]
check-all-yaml:
    @just check-yaml .yamllint *.yml

[group('check')]
check-yaml-format +PATHS:
    yamllint {{ PATHS }}
