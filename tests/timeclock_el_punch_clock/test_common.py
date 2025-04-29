import pathlib
import re

import hypothesis

from conftest import (
    log_timeclock_contents,
    clock_in_lines,
    clock_out_lines,
    log_timeclocks,
)

_clock_in_line_pattern = re.compile(
    r"i\s+[0-9]{4}-[0-9]{2}-[0-9]{2}\s+[0-9]{2}:[0-9]{2}:[0-9]{2}\s*.*\n"
)
_clock_out_line_pattern = re.compile(
    r"o\s+[0-9]{4}-[0-9]{2}-[0-9]{2}\s+[0-9]{2}:[0-9]{2}:[0-9]{2}\n"
)


def test_clock_in_line_pattern_does_not_match_any() -> None:
    assert not _clock_in_line_pattern.match("does not match")


def test_clock_out_line_pattern_does_not_match_any() -> None:
    assert not _clock_in_line_pattern.match("does not match")


@hypothesis.given(clock_in_lines())
def test_clock_in_lines_matches(clock_in_line) -> None:
    assert _clock_in_line_pattern.match(clock_in_line) is not None


@hypothesis.given(clock_out_lines())
def test_clock_out_lines_matches(clock_out_line) -> None:
    assert _clock_out_line_pattern.match(clock_out_line) is not None


@hypothesis.given(log_timeclock_contents(max_size=64))
def test_log_timeclock_contents_in_order(log_timeclock_content: str) -> None:
    lines = [
        line[len("i ") : (len("i YYYY-mm-dd HH:MM:SS"))]
        for line in log_timeclock_content.splitlines()
        if line.startswith("i") or line.startswith("o")
    ]
    assert lines == sorted(lines)


@hypothesis.given(log_timeclock_contents(max_size=64))
def test_log_timeclock_contents_alternating(log_timeclock_content: str) -> None:
    lines = log_timeclock_content.splitlines()
    lines = [line[0] for line in lines if line.startswith("i") or line.startswith("o")]
    pred = "o"
    for line in lines:
        assert line != pred
        pred = line


@hypothesis.given(log_timeclocks(max_size=64))
def test_log_timeclock_is_writeable_file(log_timeclock: pathlib.Path) -> None:
    assert log_timeclock.is_file()
    with log_timeclock.open("w") as log_timeclock_file:
        assert log_timeclock_file.writable()
