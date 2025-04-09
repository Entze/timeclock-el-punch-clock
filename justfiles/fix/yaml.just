[group('fix')]
fix-yaml +PATHS:
    @just fix-yaml-format {{ PATHS }}

[group('fix')]
fix-all-yaml:
    @just fix-yaml .yamllint *.yml

[group('fix')]
fix-yaml-format +PATHS:
    #!/usr/bin/env sh
    for path in {{ PATHS }}; do
        yq --prettyPrint --inplace $path
    done
