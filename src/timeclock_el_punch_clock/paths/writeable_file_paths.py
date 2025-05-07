import pathlib
from typing import NewType

import deal

from timeclock_el_punch_clock.paths.errors import (
    PathDoesNotExist,
    PathNotAFileError,
    PathNotWriteableError,
)

WriteableFilePath = NewType("WriteableFilePath", pathlib.Path)


@deal.has("io")
@deal.raises(
    PathDoesNotExist,
    PathNotAFileError,
    PathNotWriteableError,
)
def from_path(path: pathlib.Path) -> WriteableFilePath:
    if not path.exists(follow_symlinks=True):
        raise PathDoesNotExist(f'"{path}" does not exist')
    if not path.is_file():
        raise PathNotAFileError(f'"{path}" is not a file')
    try:
        with path.open("w") as file:
            if not file.writable():
                raise PathNotWriteableError(f'"{path}" is not writable')
    except PermissionError as err:
        raise PathNotWriteableError(f'"{path}" is not writable') from err
    return WriteableFilePath(path)
