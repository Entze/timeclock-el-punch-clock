import datetime

import hypothesis

from conftest import clock_in_commands
from timeclock_el_punch_clock.accounts import Account
from timeclock_el_punch_clock.commands.clock_in import ClockIn
from timeclock_el_punch_clock.paths.writeable_file_paths import WriteableFilePath


def test_call_with_empty_log_timeclock_ensures_at_least_one_line_and_last_line_is_expected(
    empty_log_timeclock,
) -> None:
    file = WriteableFilePath(empty_log_timeclock)
    command = ClockIn(
        file=file,
        datetimestamp=datetime.datetime(1970, 1, 1, 12, 0, 0),
        accounts=(Account("INBOX"), Account("meeting")),
        delimiter=":",
    )

    command()

    lines = 0
    with file.open(mode="r") as file:
        for line in file:
            lines += 1

    assert lines > 0
    expected = "i 1970-01-01 12:00:00 INBOX:meeting\n"
    assert line == expected


def test_call_with_clocked_out_log_timeclock_ensures_at_least_one_line_and_last_line_is_expected(
    clocked_out_log_timeclock,
) -> None:
    file = WriteableFilePath(clocked_out_log_timeclock)
    command = ClockIn(
        file=file,
        datetimestamp=datetime.datetime(1970, 1, 1, 12, 0, 0),
        accounts=(Account("INBOX"), Account("meeting")),
        delimiter=":",
    )

    command()

    lines = 0
    with file.open(mode="r") as file:
        for line in file:
            lines += 1

    assert lines > 0
    expected = "i 1970-01-01 12:00:00 INBOX:meeting\n"
    assert line == expected


def test_call_with_clocked_out_log_timeclock_and_empty_accounts_ensures_at_least_one_line_and_last_line_is_expected(
    clocked_out_log_timeclock,
) -> None:
    file = WriteableFilePath(clocked_out_log_timeclock)
    command = ClockIn(
        file=file,
        datetimestamp=datetime.datetime(1970, 1, 1, 12, 0, 0),
        accounts=(),
        delimiter=":",
    )

    command()

    lines = 0
    with file.open(mode="r") as file:
        for line in file:
            lines += 1

    assert lines > 0
    expected = "i 1970-01-01 12:00:00\n"
    assert line == expected


@hypothesis.given(clock_in_commands(log_timeclock_max_size=64))
def test_call_ensures_at_least_one_line_and_last_line_is_expected(
    command: ClockIn,
) -> None:
    command()

    lines = 0
    with command.file.open(mode="r") as file:
        for line in file:
            lines += 1

    assert lines > 0
    accounts_ = ""
    if command.accounts:
        accounts_ = f" {command.delimiter.join(command.accounts)}"
    expected = f"i {command.datetimestamp.strftime('%Y-%m-%d %H:%M:%S')}{accounts_}\n"
    assert line == expected
