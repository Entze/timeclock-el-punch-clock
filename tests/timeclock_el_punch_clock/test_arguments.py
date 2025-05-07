import argparse
import datetime
import pathlib
import stat
import tempfile
from unittest import mock

import pytest

from timeclock_el_punch_clock.paths import writeable_file_paths
from timeclock_el_punch_clock.arguments import Arguments

_default_datetimestamp = datetime.datetime(1970, 1, 1, 0, 0, 0)


def test_from_namespace_with_empty_namespace_returns_default() -> None:
    namespace = argparse.Namespace()
    with (
        tempfile.NamedTemporaryFile(mode="w") as file,
        mock.patch.object(
            Arguments, "default_file", return_value=pathlib.Path(file.name)
        ),
        mock.patch.object(
            Arguments, "default_datetimestamp", return_value=_default_datetimestamp
        ),
    ):
        expected = Arguments(
            file=writeable_file_paths.from_path(Arguments.default_file()),
            datetimestamp=Arguments.default_datetimestamp(),
            accounts=Arguments.default_accounts(),
            delimiter=Arguments.default_delimiter(),
        )

        actual = Arguments.from_namespace(namespace)

    assert actual == expected


def test_from_namespace_with_file_returns_command_with_file() -> None:
    with tempfile.NamedTemporaryFile(mode="w") as file:
        path = pathlib.Path(file.name)
        namespace = argparse.Namespace(file=path)
        with mock.patch.object(
            Arguments, "default_datetimestamp", return_value=_default_datetimestamp
        ):
            expected = Arguments(
                file=writeable_file_paths.from_path(
                    writeable_file_paths.from_path(path)
                ),
                datetimestamp=Arguments.default_datetimestamp(),
                accounts=Arguments.default_accounts(),
                delimiter=Arguments.default_delimiter(),
            )

            actual = Arguments.from_namespace(namespace)

    assert actual == expected


def test_from_namespace_with_non_existing_file_raises_exception_group_with_path_does_not_exist() -> (
    None
):
    path = pathlib.Path("file-does-not-exist.txt")
    namespace = argparse.Namespace(file=path)

    with pytest.raises(ExceptionGroup) as excinfo:
        Arguments.from_namespace(namespace)
        assert str(path) in excinfo.value, (
            f"ExceptionGroup shows the path: {excinfo.value}"
        )
        assert "does not exist" in excinfo.value, (
            f"ExceptionGroup shows the reason: {excinfo.value}"
        )


def test_from_namespace_with_directory_raises_exception_group_with_not_a_file_error() -> (
    None
):
    with tempfile.TemporaryDirectory() as directory:
        path = pathlib.Path(directory)
        namespace = argparse.Namespace(file=path)

        with pytest.raises(ExceptionGroup) as excinfo:
            Arguments.from_namespace(namespace)
            assert str(path) in excinfo.value, (
                f"ExceptionGroup.value shows the path: {excinfo.value}"
            )
            assert "is not a file" in excinfo.value, (
                f"ExceptionGroup shows the reason: {excinfo.value}"
            )


def test_from_namespace_with_non_readable_file_raises_exception_group_with_not_writeable_error() -> (
    None
):
    with tempfile.NamedTemporaryFile(mode="r") as file:
        path = pathlib.Path(file.name)
        path.chmod(stat.S_IREAD)
        namespace = argparse.Namespace(file=path)

        with pytest.raises(ExceptionGroup) as excinfo:
            Arguments.from_namespace(namespace)
            assert str(path) in excinfo.value, (
                f"ExceptionGroup.value shows the path: {excinfo.value}"
            )
            assert "is not writeable" in excinfo.value, (
                f"ExceptionGroup shows the reason: {excinfo.value}"
            )


def test_from_namespace_with_datetimestamp_returns_command_with_datetimestamp() -> None:
    datetimestamp = datetime.datetime(2000, 1, 1, 12, 0, 0)
    namespace = argparse.Namespace(datetime=datetimestamp)
    with (
        tempfile.NamedTemporaryFile(mode="w") as file,
        mock.patch.object(
            Arguments, "default_file", return_value=pathlib.Path(file.name)
        ),
    ):
        expected = Arguments(
            file=writeable_file_paths.from_path(Arguments.default_file()),
            datetimestamp=datetimestamp,
            accounts=Arguments.default_accounts(),
            delimiter=Arguments.default_delimiter(),
        )

        actual = Arguments.from_namespace(namespace)

    assert actual == expected
