[group('check')]
check-justfile +PATHS:
    @just check-justfile-format {{ PATHS }}

[group('check')]
check-all-justfile:
    @just check-justfile justfile justfiles/**/*.just

[group('check')]
check-justfile-format +PATHS:
    #!/usr/bin/env sh
    for path in {{ PATHS }}; do
        just --unstable --fmt --check --justfile $path
    done
