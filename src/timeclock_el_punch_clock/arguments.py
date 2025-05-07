import argparse
import datetime
import pathlib
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Self, MutableSequence, Callable

import deal

import timeclock_el_punch_clock.paths.writeable_file_paths as writeable_file_paths
from timeclock_el_punch_clock.accounts import Account, into_accounts
from timeclock_el_punch_clock.paths.errors import (
    PathDoesNotExist,
    PathNotAFileError,
    PathNotWriteableError,
)
from timeclock_el_punch_clock.paths.writeable_file_paths import WriteableFilePath


def _parse_from_namespace[T, V](
    namespace: argparse.Namespace,
    attr: str,
    default_factory: Callable[[], T],
    parse: Callable[[T], V],
) -> V:
    unparsed_arg: T = default_factory()
    if hasattr(namespace, attr):
        unparsed_arg = getattr(namespace, attr)
    return parse(unparsed_arg)


def _get_from_namespace[V](
    namespace: argparse.Namespace,
    attr: str,
    default_factory: Callable[[], V],
) -> V:
    if hasattr(namespace, attr):
        return getattr(namespace, attr)
    return default_factory()


_ArgumentsFileError = PathDoesNotExist | PathNotAFileError | PathNotWriteableError
_ArgumentsFileErrors = (PathDoesNotExist, PathNotAFileError, PathNotWriteableError)
_ArgumentsError = _ArgumentsFileError


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
    def default_accounts() -> Sequence[str]:
        return ()

    @staticmethod
    def default_delimiter() -> str:
        return ":"

    @classmethod
    @deal.has("io")
    @deal.raises(ExceptionGroup)
    def from_namespace(cls, namespace: argparse.Namespace) -> Self:
        errors: MutableSequence[_ArgumentsError] = []

        file: WriteableFilePath | None = None
        datetimestamp: datetime.datetime
        accounts: Sequence[Account]
        delimiter: str | None = None

        try:
            file = _parse_from_namespace(
                namespace,
                attr="file",
                default_factory=cls.default_file,
                parse=writeable_file_paths.from_path,
            )
        except _ArgumentsFileErrors as err:
            errors.append(err)
        datetimestamp = _get_from_namespace(
            namespace,
            attr="datetime",
            default_factory=cls.default_datetimestamp,
        )
        accounts = _parse_from_namespace(
            namespace,
            attr="accounts",
            default_factory=cls.default_accounts,
            parse=into_accounts,
        )

        if errors:
            raise ExceptionGroup(
                f"Could not parse namespace {namespace} into Arguments", tuple(errors)
            )
        assert not errors, "Invariant: errors is empty"
        assert file is not None, "Invariant: file is not None, if errors is empty"

        delimiter = cls.default_delimiter()

        return cls(
            file=file,
            datetimestamp=datetimestamp,
            accounts=accounts,
            delimiter=delimiter,
        )
