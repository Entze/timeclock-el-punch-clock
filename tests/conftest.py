import pathlib

import pytest

clocked_out_log_timeclock_contents = """* 1970
** 1970-01

*** 1970-01-01

i 1970-01-01 00:00:00 unix-epoch:start
o 1970-01-01 00:00:00
"""

clocked_in_log_timeclock_contents = """* 1970

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
        file.write(clocked_out_log_timeclock_contents)
    return path


@pytest.fixture
def clocked_in_log_timeclock(tmp_path_factory) -> pathlib.Path:
    path = tmp_path_factory.getbasetemp() / "log.timeclock"
    with path.open("w") as file:
        file.write(clocked_in_log_timeclock_contents)
    return path
