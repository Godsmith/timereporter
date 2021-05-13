import os
from pathlib import Path

from timereporter.__main__ import main


def test_use_alias_raises_no_error(custom_log_path):
    custom_log_path(
        Path(os.path.realpath(__file__)).parent / "_fixtures" / "alias.yaml"
    )

    _, err = main("slw")

    assert err == 0


def test_list_aliases(custom_log_path):
    custom_log_path(
        Path(os.path.realpath(__file__)).parent / "_fixtures" / "alias.yaml"
    )

    out, _ = main("alias")

    assert "slw" in out
    assert "show last week" in out


class TestAdd:
    def test_add_alias(self, custom_log_path):
        custom_log_path(
            Path(os.path.realpath(__file__)).parent / "_fixtures" / "alias.yaml"
        )
        main("alias hello came 7:45")

        _, err = main("hello")

        assert err == 0

    def test_add_alias_but_no_definition_throws_error(self, custom_log_path):
        custom_log_path(
            Path(os.path.realpath(__file__)).parent / "_fixtures" / "alias.yaml"
        )
        out, err = main("alias hello")

        assert err == 1
        assert "Error: new alias lacks definition." in out


class TestRemove:
    def test_removing_something_that_does_not_exist_raises_error(self):
        out, err = main("alias --remove foo")

        assert err == 1
        assert "Error: alias 'foo' does not exist." in out

    def test_remove(self, custom_log_path):
        custom_log_path(
            Path(os.path.realpath(__file__)).parent / "_fixtures" / "alias.yaml"
        )
        main("alias --remove slw")
        out, err = main("alias")

        assert err == 0
        assert "slw" not in out
