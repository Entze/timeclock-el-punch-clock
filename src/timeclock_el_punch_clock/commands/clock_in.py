from __future__ import annotations

import datetime
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Self

import deal

from timeclock_el_punch_clock.accounts import Account
from timeclock_el_punch_clock.arguments import Arguments
from timeclock_el_punch_clock.paths.writeable_file_paths import WriteableFilePath


def _clock_in__call___ensure(self: ClockIn, result: None) -> bool:
    lines = 0
    line: str | None = None
    with self.file.open(mode="r") as file:
        for line in file:
            lines += 1
    accounts = ""
    if self.accounts:
        accounts = f" {self.delimiter.join(self.accounts)}"
    in_line = f"i {self.datetimestamp.strftime('%Y-%m-%d %H:%M:%S')}{accounts}\n"
    return lines > 0 and line is not None and line == in_line


@dataclass
class ClockIn:
    file: WriteableFilePath
    datetimestamp: datetime.datetime
    accounts: Sequence[Account]
    delimiter: str

    @classmethod
    def from_arguments(cls, arguments: Arguments) -> Self:
        raise NotImplementedError

    @deal.has("io")
    @deal.ensure(_clock_in__call___ensure)
    def __call__(self) -> None:
        accounts = ""
        if self.accounts:
            accounts = f" {self.delimiter.join(self.accounts)}"
        line: str = f"i {self.datetimestamp.strftime('%Y-%m-%d %H:%M:%S')}{accounts}\n"
        with self.file.open(mode="a") as file:
            file.write(line)
