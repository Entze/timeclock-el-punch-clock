import pytest

import timeclock_el_punch_clock.cli as pc


def test_import_ensures_top():
    pass


def test_run_with_help_guarantees_system_exit_0():
    with pytest.raises(SystemExit) as system_exit:
        pc.main(("--help",))
    assert system_exit.value.code == 0
