from timereporter.__main__ import main


class TestUndo:
    def test_undo(self):
        s, _ = main("came 9")
        assert "9:00" in s
        s, _ = main("undo")
        assert "9:00" not in s

    def test_redo(self):
        main("came 9")
        main("undo")
        s, _ = main("redo")
        assert "9:00" in s

    def test_undo_command_affecting_multiple_days(self):
        main("monday tuesday came 9")
        s, _ = main("undo")
        assert "9:00" not in s

    def test_redo_command_affecting_multiple_days(self):
        main("monday tuesday came 9")
        main("undo")
        s, _ = main("redo")
        assert s.count("9:00") == 2

    def test_undoing_without_having_anything_to_undo_shall_not_crash(self):
        main("undo")

    def test_no_redo_after_action(self):
        main("came 9")
        main("undo")
        main("came 8")
        s, _ = main("redo")  # This shall not overwrite the 8:00
        assert "8:00" in s

    def test_the_week_which_affected_by_the_undo_is_shown_afterwards(self):
        main("last friday came 9")
        main("last friday left 17")
        s, _ = main("undo")
        assert "9:00" in s

    def test_the_week_which_affected_by_the_redo_is_shown_afterwards(self):
        main("last friday came 9")
        main("undo")
        s, _ = main("redo")
        assert "9:00" in s
