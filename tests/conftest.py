import datetime
import pathlib
import string
import tempfile
from collections.abc import MutableSequence

import hypothesis.strategies
import pytest

from timeclock_el_punch_clock.accounts import Account
from timeclock_el_punch_clock.commands.clock_in import ClockIn
from timeclock_el_punch_clock.paths import writeable_file_paths

example_clocked_out_log_timeclock_contents = """* 1970
** 1970-01

*** 1970-01-01

i 1970-01-01 00:00:00 unix-epoch:start
o 1970-01-01 00:00:00
"""

example_clocked_in_log_timeclock_contents = """* 1970

* 1970-01

*** 1970-01-01

i 1970-01-01 00:00:00 unix-epoch:start
o 1970-01-01 00:00:00
i 1970-01-01 00:01:00 party:new-year
"""


@pytest.fixture
def empty_log_timeclock(tmp_path_factory) -> pathlib.Path:
    path = tmp_path_factory.getbasetemp() / "log.timeclock"
    with path.open("w") as file:
        file.write("")
    return path


@pytest.fixture
def clocked_out_log_timeclock(tmp_path_factory) -> pathlib.Path:
    path = tmp_path_factory.getbasetemp() / "log.timeclock"
    with path.open("w") as file:
        file.write(example_clocked_out_log_timeclock_contents)
    return path


@pytest.fixture
def clocked_in_log_timeclock(tmp_path_factory) -> pathlib.Path:
    path = tmp_path_factory.getbasetemp() / "log.timeclock"
    with path.open("w") as file:
        file.write(example_clocked_in_log_timeclock_contents)
    return path


@hypothesis.strategies.composite
def accounts(draw) -> Account:
    return Account(draw(hypothesis.strategies.text(alphabet=string.ascii_letters)))


@hypothesis.strategies.composite
def delimiters(draw) -> Account:
    return draw(hypothesis.strategies.sampled_from(string.punctuation))


@hypothesis.strategies.composite
def clock_in_lines(
    draw,
    *,
    delimiter_value=None,
    datetimestamp_value=None,
    min_datetime_value=datetime.datetime(1970, 1, 1, 0, 0, 0),
    max_datetime_value=datetime.datetime(9998, 12, 31, 23, 59, 59),
    min_accounts_size=0,
    max_accounts_size=None,
) -> str:
    datetimestamp: datetime.datetime | None = datetimestamp_value
    if datetimestamp is None:
        datetimestamp = draw(
            hypothesis.strategies.datetimes(
                min_value=min_datetime_value, max_value=max_datetime_value
            )
        )
    accounts_ = draw(
        hypothesis.strategies.lists(
            accounts(), min_size=min_accounts_size, max_size=max_accounts_size
        )
    )
    delim = delimiter_value
    if delim is None:
        delim = draw(delimiters())
    return f"i {datetimestamp.strftime('%Y-%m-%d %H:%M:%S')} {delim.join(accounts_)}\n"


@hypothesis.strategies.composite
def clock_out_lines(
    draw,
    *,
    datetimestamp_value=None,
    min_datetime_value=datetime.datetime(1970, 1, 1, 0, 0, 0),
    max_datetime_value=datetime.datetime(9998, 12, 31, 23, 59, 59),
) -> str:
    datetimestamp: datetime.datetime | None = datetimestamp_value
    if datetimestamp is None:
        datetimestamp = draw(
            hypothesis.strategies.datetimes(
                min_value=min_datetime_value, max_value=max_datetime_value
            )
        )
    return f"o {datetimestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"


@hypothesis.strategies.composite
def log_timeclock_contents(
    draw,
    *,
    datetime_min_value=datetime.datetime(1970, 1, 1, 0, 0, 0),
    datetime_max_value=datetime.datetime(9998, 12, 31, 23, 59, 59),
    delimiter_value=None,
    min_size=0,
    max_size=None,
) -> str:
    statements: MutableSequence[str] = []
    datetimestamp_min_value = datetime_min_value
    datetimestamp_max_value = datetime_max_value
    if max_size is None:
        max_size = draw(hypothesis.strategies.integers(min_value=min_size))
    size = draw(hypothesis.strategies.integers(min_value=min_size, max_value=max_size))
    span = datetimestamp_max_value.timestamp() - datetimestamp_min_value.timestamp()
    datetimestamp_max_value = datetime.datetime.fromtimestamp(
        datetimestamp_min_value.timestamp() + (span / (size + 1))
    )
    delimiter = delimiter_value
    if delimiter is None:
        delimiter = draw(delimiters())
    draw_clock_in = True
    for size in range(size):
        datetimestamp: datetime.datetime = draw(
            hypothesis.strategies.datetimes(
                min_value=datetimestamp_min_value, max_value=datetimestamp_max_value
            )
        )
        if draw_clock_in:
            statements.append(
                draw(
                    clock_in_lines(
                        datetimestamp_value=datetimestamp, delimiter_value=delimiter
                    )
                )
            )
        else:
            statements.append(draw(clock_out_lines(datetimestamp_value=datetimestamp)))
        datetimestamp_min_value = datetimestamp_max_value
        span = datetime_max_value.timestamp() - datetimestamp_min_value.timestamp()
        datetimestamp_max_value = datetime.datetime.fromtimestamp(
            datetimestamp_min_value.timestamp() + (span / ((max_size + 1) - size))
        )
        draw_clock_in = not draw_clock_in
    return "".join(statements)


@hypothesis.strategies.composite
def log_timeclocks(
    draw,
    *,
    datetime_min_value=datetime.datetime(1970, 1, 1, 0, 0, 0),
    datetime_max_value=datetime.datetime(9998, 12, 31, 23, 59, 59),
    min_size=0,
    max_size=None,
    delimiter_value=None,
) -> pathlib.Path:
    contents = draw(
        log_timeclock_contents(
            datetime_min_value=datetime_min_value,
            datetime_max_value=datetime_max_value,
            min_size=min_size,
            max_size=max_size,
            delimiter_value=delimiter_value,
        )
    )
    _, path = tempfile.mkstemp()
    path = pathlib.Path(path)
    path.write_text(contents)
    return path


@hypothesis.strategies.composite
def clock_in_commands(
    draw,
    *,
    datetime_min_value=datetime.datetime(1970, 1, 1, 0, 0, 0),
    datetime_max_value=datetime.datetime(9998, 12, 31, 23, 59, 59),
    log_timeclock_min_size=0,
    log_timeclock_max_size=None,
    delimiter_value=None,
    accounts_value=None,
    accounts_min_size=0,
    accounts_max_size=None,
) -> ClockIn:
    delimiter = delimiter_value
    if delimiter is None:
        delimiter = draw(delimiters())
    accounts_ = accounts_value
    if accounts_ is None:
        accounts_ = draw(
            hypothesis.strategies.lists(
                accounts(), min_size=accounts_min_size, max_size=accounts_max_size
            )
        )

    log_timeclock = draw(
        log_timeclocks(
            datetime_min_value=datetime_min_value,
            datetime_max_value=datetime_max_value,
            min_size=log_timeclock_min_size,
            max_size=log_timeclock_max_size,
            delimiter_value=delimiter,
        )
    )
    file = writeable_file_paths.from_path(log_timeclock)
    return ClockIn(
        file=file,
        datetimestamp=draw(hypothesis.strategies.datetimes()),
        accounts=accounts_,
        delimiter=delimiter,
    )
