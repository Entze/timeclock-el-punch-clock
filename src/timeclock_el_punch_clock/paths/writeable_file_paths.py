import pathlib
from typing import NewType

import deal

from timeclock_el_punch_clock.paths.errors import NotAFileError, NotWriteableError

WriteableFilePath = NewType("WriteableFilePath", pathlib.Path)


@deal.has("io")
@deal.raises(
    FileNotFoundError,
    NotAFileError,
    NotWriteableError,
    OSError,  # open
)
def from_path(path: pathlib.Path) -> WriteableFilePath:
    if not path.exists(follow_symlinks=True):
        raise FileNotFoundError(path)
    if not path.is_file():
        raise NotAFileError(f'"{path}" is not a file')

    with path.open("w") as file:
        if not file.writable():
            raise NotWriteableError(f'"{path}" is not writable')
    return WriteableFilePath(path)
