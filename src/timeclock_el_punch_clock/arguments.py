from dataclasses import dataclass

import pathlib


@dataclass(frozen=True)
class Arguments:
    file: pathlib.Path
