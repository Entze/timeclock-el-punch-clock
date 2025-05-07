import argparse
import datetime
import pathlib
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Self, MutableSequence, Callable

import deal

import timeclock_el_punch_clock.paths.writeable_file_paths as writeable_file_paths
from timeclock_el_punch_clock.accounts import Account
from timeclock_el_punch_clock.paths.errors import NotAFileError, NotWriteableError
from timeclock_el_punch_clock.paths.writeable_file_paths import WriteableFilePath

@dataclass(frozen=True)
class Arguments:
    file: WriteableFilePath
    datetimestamp: datetime.datetime
    accounts: Sequence[Account]
    delimiter: str

    @staticmethod
    def default_file() -> pathlib.Path:
        return pathlib.Path("log.timeclock")

    @staticmethod
    def default_datetimestamp() -> datetime.datetime:
        return datetime.datetime.now()

    @staticmethod
    def default_accounts() -> Sequence[Account]:
        return ()

    @staticmethod
    def default_delimiter() -> str:
        return ":"

    @classmethod
    @deal.has("io")
    @deal.raises(ExceptionGroup)
    def from_namespace(cls, namespace: argparse.Namespace) -> Self:
        # errors: MutableSequence[_ArgumentsError] = []

        file: WriteableFilePath
        datetimestamp: datetime.datetime
        accounts: Sequence[Account]
        delimiter: str

        file = writeable_file_paths.from_path(cls.default_file())
        datetimestamp = cls.default_datetimestamp()
        accounts = cls.default_accounts()
        delimiter = cls.default_delimiter()

        return cls(file=file, datetimestamp=datetimestamp, accounts=accounts, delimiter=delimiter)
