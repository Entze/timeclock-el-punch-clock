import argparse
import datetime
import pathlib
import tempfile
from unittest import mock

from timeclock_el_punch_clock.paths import writeable_file_paths
from timeclock_el_punch_clock.arguments import Arguments

_default_datetimestamp = datetime.datetime(1970, 1, 1, 0, 0, 0)

def test_from_namespace_with_empty_namespace_returns_default() -> None:
    namespace = argparse.Namespace()
    with (tempfile.NamedTemporaryFile(mode='w') as file,
          mock.patch.object(Arguments, "default_file", return_value=pathlib.Path(file.name)),
          mock.patch.object(Arguments, "default_datetimestamp", return_value=_default_datetimestamp)):
        expected = Arguments(
            file=writeable_file_paths.from_path(Arguments.default_file()),
            datetimestamp=Arguments.default_datetimestamp(),
            accounts=Arguments.default_accounts(),
            delimiter=Arguments.default_delimiter(),
        )

        actual = Arguments.from_namespace(namespace)

    assert actual == expected


def test_from_namespace_with_file_returns_command_with_file() -> None:
    with tempfile.NamedTemporaryFile(mode='w') as file:
        path = pathlib.Path(file.name)
        namespace = argparse.Namespace(file=path)
        with (mock.patch.object(Arguments, "default_datetimestamp", return_value=_default_datetimestamp)):
            expected = Arguments(
                file=writeable_file_paths.from_path(writeable_file_paths.from_path(path)),
                datetimestamp=Arguments.default_datetimestamp(),
                accounts=Arguments.default_accounts(),
                delimiter=Arguments.default_delimiter(),
            )

            actual = Arguments.from_namespace(namespace)

    assert actual == expected

