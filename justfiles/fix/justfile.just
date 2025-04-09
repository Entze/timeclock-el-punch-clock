[group('fix')]
fix-justfile +PATHS:
    @just fix-justfile-format {{ PATHS }}

[group('fix')]
fix-all-justfile:
    @just fix-justfile justfile justfiles/**/*.just

[group('fix')]
fix-justfile-format +PATHS:
    #!/usr/bin/env sh
    for path in {{ PATHS }}; do
        just --unstable --fmt --justfile $path
    done
